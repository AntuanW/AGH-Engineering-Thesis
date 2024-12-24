import logging
import re
from typing import NamedTuple

from bson.objectid import ObjectId
from fastapi import Depends

from app.config_download.config_download_service import ConfigDownloadService
from app.config_download.utils.download_config_request import DownloadConfigRequest
from app.config_download.utils.downloaded_config import DownloadedConfig
from app.models.connection import ConnectionModel
from app.models.mapped_device import MappedDeviceModel
from app.models.mapping import MappingCollectionModel, MappingType
from app.models.rack import RackModel
from app.models.topology import TopologyModel
from app.repository.device_repository import DeviceRepository
from app.repository.lab_group_repository import LabGroupRepository
from app.repository.mapping_repository import MappingRepository
from app.repository.topology_repository import TopologyRepository
from app.models.device import DeviceModel, Interface, InterfaceType
from app.running_config.util.device_config_types import DeviceConfigInfo, DeviceType


class MapWithSubs(NamedTuple):
    mapped_device: MappedDeviceModel
    substitutions: dict[Interface, Interface]



class MappingService:
    def __init__(self,
                 lab_group_repo: LabGroupRepository = Depends(LabGroupRepository),
                 device_repo: DeviceRepository = Depends(DeviceRepository),
                 topology_repo: TopologyRepository = Depends(TopologyRepository),
                 mapping_repo: MappingRepository = Depends(MappingRepository),
                 download_service: ConfigDownloadService = Depends(ConfigDownloadService)):
        self._lab_group_repo = lab_group_repo
        self._device_repo = device_repo
        self._topology_repo = topology_repo
        self._mapping_repo = mapping_repo
        self._download_service = download_service

    def get_device_mappings(self, topology_id: str, group_numbers: list[int] | None) -> MappingCollectionModel:
        """
        Creates and returns a topology equivalent to :param topology_id: using laboratory devices.
        :param topology_id: ID of a topology extracted from PKT file.
        :param group_numbers: Groups for which the mapping is calculated.
        """

        topology_id = ObjectId(topology_id)
        topology = self._topology_repo.find_object({"_id": topology_id})

        if group_numbers is None:
            group_numbers = self._lab_group_repo.get_all_group_ids()

        mapping_collection = MappingCollectionModel(name=topology.name,
                                                    type=MappingType.CREATED_FROM_PKT,
                                                    topology_id=str(topology_id))
        for group_number in group_numbers:
            mapped_devices = self._get_device_mapping_for_lab_group(topology, group_number)
            mapping_collection.mappings[group_number] = mapped_devices

        self._mapping_repo.upsert({
            "topology_id": topology_id,
            "name": mapping_collection.name
        },
        mapping_collection.model_dump())

        return mapping_collection

    def _get_device_mapping_for_lab_group(self, topology: TopologyModel, group_number: int) -> list[MappedDeviceModel]:
        group = self._lab_group_repo.find_object({"lab_group_number": group_number})
        if group is None:
            raise KeyError(f"Group {group} does not exist.")

        mapped_devices = self._map_devices_by_criteria(topology, group.rack)
        mapped_devices = self._map_device_connections(topology, mapped_devices)
        mapped_devices = self._substitute_running_configs(mapped_devices)

        return [md.mapped_device for name, md in mapped_devices.items()]

    def _map_devices_by_criteria(self,
                                 topology: TopologyModel,
                                 rack: RackModel) -> dict[str, MapWithSubs]:

        available_rack_devices: list[DeviceModel] = self._device_repo.find_objects({"rack_id": rack.rack_id})
        available_rack_ports = rack.config_ports[::-1]  # so that smallest ports are popped from end of list in O(1)

        mapped_devices = {}
        for device_info in topology.topology:
            port = available_rack_ports.pop(-1)
            available_device, iface_substitutions = self._find_best_available_device(device_info, available_rack_devices, rack.rack_id)
            available_rack_devices.remove(available_device)

            mapped_device = MappedDeviceModel(
                name=available_device.name,
                device_type=device_info.dev_type,
                netmiko_device_type=device_info.dev_type.to_netmiko_device_type(),
                ip_address=rack.config_port_ip_address,
                port=port,
                neighbours=[],
                mapped_config=device_info.dev_running_config,
            )
            mapped_devices[device_info.dev_id] = MapWithSubs(mapped_device, iface_substitutions)

        return mapped_devices

    def _find_best_available_device(self, requirements: DeviceConfigInfo, available_devices: list[DeviceModel], rack_id: int) -> MapWithSubs:
        # Remove devices of wrong type
        available_devices = [dev for dev in available_devices if dev.device_type == requirements.dev_type]

        if requirements.dev_type == DeviceType.PC:
            try:
                return MapWithSubs(
                    available_devices[0],
                    {Interface(requirements.dev_neighbours[0].from_if): available_devices[0].interfaces[0]}
                )
            except IndexError:
                raise ValueError(f"No available PCs on rack {rack_id} or any available has no matching interfaces")

        # Find devices with matching interfaces
        available_matching_ifs = []
        required_interfaces = set(Interface(conn.from_if) for conn in requirements.dev_neighbours)
        for device in available_devices:
            if required_interfaces.issubset(device.interfaces):
                available_matching_ifs.append(device)
        # Greedily pick one with the least other interfaces
        if len(available_matching_ifs) > 0:
            best_device =  min(available_matching_ifs, key=lambda dev: len(dev.interfaces))
            return MapWithSubs(best_device, {})

        # If there is none available, try substituting Gi and Fa
        for device in available_devices:
            missing_interfaces = required_interfaces.difference(device.interfaces)
            for missing_iface in missing_interfaces:
                if missing_iface.type not in (InterfaceType.GI, InterfaceType.FA):
                    break
            else:
                # All missing are GI or FA, so the device can be substituted
                substitutions = {iface: self._find_best_interface_replacement(iface, device) for iface in missing_interfaces}
                logging.warn(f"No exact match for {requirements.dev_name} found on rack {rack_id}, but a Gi/Fa replacement was mapped.")
                return MapWithSubs(device, substitutions)

        raise ValueError(f"No valid mapping found for {requirements.dev_name} on rack {rack_id}.")

    def _find_best_interface_replacement(self, matched_interface: Interface, device: DeviceModel) -> Interface:
        target_port = matched_interface.port_number()
        # try the same type but different prefix
        for device_interface in device.interfaces:
            if device_interface.type == matched_interface.type and device_interface.port_number() == target_port:
                return device_interface

        # try the same type but different port
        for device_interface in device.interfaces:
            if device_interface.type == matched_interface.type:
                return device_interface

        # try another compatible type with same port
        for device_interface in device.interfaces:
            if device_interface.type in matched_interface.type.compatible_types() and device_interface.port_number() == target_port:
                return device_interface

        # try another compatible type with different port
        for device_interface in device.interfaces:
            if device_interface.type in matched_interface.type.compatible_types():
                return device_interface

    def _map_device_connections(self,
                                topology: TopologyModel,
                                mapped_devices: dict[str, MapWithSubs]) -> dict[str, MapWithSubs]:

        # TODO: Despaghettify code
        for device_info in topology.topology:
            connections = []
            for neighbour in device_info.dev_neighbours:
                origin_name = mapped_devices[device_info.dev_id].mapped_device.name
                neighbour_name = mapped_devices[neighbour.to_id].mapped_device.name
                from_interface = mapped_devices[neighbour.from_id].substitutions.get(Interface(neighbour.from_if)) or neighbour.from_if
                to_interface = mapped_devices[neighbour.to_id].substitutions.get(Interface(neighbour.to_if)) or neighbour.to_if
                connections.append(ConnectionModel(origin_name=origin_name, neighbour_name=neighbour_name, from_interface=str(from_interface), to_interface=str(to_interface)))

            mapped_devices[device_info.dev_id].mapped_device.neighbours = connections

        return mapped_devices

    def _substitute_running_configs(self, mapped_devices: dict[str, MapWithSubs]) -> dict[str, MapWithSubs]:
        for map_with_subs in mapped_devices.values():
            for sub_from, sub_to in map_with_subs.substitutions.items():
                running_config = map_with_subs.mapped_device.mapped_config
                f = str(sub_from)
                t = str(sub_to)
                for i in range(len(running_config)):
                    running_config[i] = running_config[i].replace(f, t)

        return mapped_devices

    def upsert_mapping_from_downloaded_config(self, request: DownloadConfigRequest, downloaded_configs: list[DownloadedConfig]):
        mcm = self._mapping_repo.find_mapping_by_name(request.lab_name) \
              or MappingCollectionModel(name=request.lab_name, type=MappingType.DOWNLOADED, topology_id=None)
        assert mcm.type == MappingType.DOWNLOADED

        group_info = self._lab_group_repo.find_object({"lab_group_number": request.lab_group})
        for i, device in enumerate(downloaded_configs):
            mapped_device = MappedDeviceModel(
                name=re.match(r"hostname ([a-zA-Z]+)", device.config)[0],
                ip_address=group_info.rack.config_port_ip_address,
                port=group_info.rack.config_ports[i],
                device_type=device.device_type,
                netmiko_device_type=device.device_type.to_netmiko_device_type(),
                neighbours=device.neighbours.copy(),
                mapped_config=device.config.split("\n")
            )
            mcm.mappings[request.lab_group].append(mapped_device)

        self._mapping_repo.upsert({"name": request.lab_name}, mcm)
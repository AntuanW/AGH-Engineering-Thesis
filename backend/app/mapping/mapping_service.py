from bson.objectid import ObjectId
from fastapi import Depends

from app.models.connection import ConnectionModel
from app.models.lab_group import LabGroupModel
from app.models.mapped_device import MappedDeviceModel
from app.models.mapping import MappingModel
from app.models.rack import RackModel
from app.models.topology import TopologyModel
from app.repository.device_repository import DeviceRepository
from app.repository.lab_group_repository import LabGroupRepository
from app.repository.topology_repository import TopologyRepository
from app.models.device import DeviceModel


class MappingService:
    def __init__(self,
                 lab_group_repo: LabGroupRepository = Depends(LabGroupRepository),
                 device_repo: DeviceRepository = Depends(DeviceRepository),
                 topology_repo: TopologyRepository = Depends(TopologyRepository)):
        self._lab_group_repo = lab_group_repo
        self._device_repo = device_repo
        self._topology_repo = topology_repo

    def get_device_mappings(self, topology_id: str, group_numbers: list[int]) -> list[MappingModel]:
        topology_id = ObjectId(topology_id)
        topology = self._topology_repo.find_object({"_id": topology_id})

        mapping_list = []
        for group_number in group_numbers:
            mapped_devices = self._get_device_mapping_for_lab_group(topology, group_number)
            mapping_list.append(MappingModel(
                lab_group=group_number,
                mapped_devices=mapped_devices
            ))

        return mapping_list

    def _get_device_mapping_for_lab_group(self, topology: TopologyModel, group_number: int) -> list[MappedDeviceModel]:
        group = self._lab_group_repo.find_object({"group_number": group_number})
        if group is None:
            raise KeyError(f"Group {group} does not exist.")

        mapped_devices = self._map_devices_by_criteria(topology, group.rack)
        mapped_devices = self._map_device_connections(topology, mapped_devices)

        return list(mapped_devices.values())

    def _map_devices_by_criteria(self,
                                 topology: TopologyModel,
                                 rack: RackModel) -> dict[str, MappedDeviceModel]:

        available_rack_devices: list[DeviceModel] = self._device_repo.find_objects({"rack_id": rack.rack_id})
        available_rack_ports = rack.config_ports[::-1]  # so that smallest ports are popped from end of list in O(1)

        mapped_devices = {}
        for device_info in topology.topology:
            port = available_rack_ports.pop(-1)

            for available_device in available_rack_devices:
                if available_device.device_type == device_info.dev_type:
                    available_rack_devices.remove(available_device)
                    break
            else:
                raise ValueError(f"There is no device matching required criteria")

            mapped_device = MappedDeviceModel(
                name=available_device.name,
                netmiko_device_type=device_info.dev_type.to_netmiko_device_type(),
                ip_address=rack.config_port_ip_address,
                port=port,
                neighbours=[],
                mapped_config=device_info.dev_running_config,
            )
            mapped_devices[device_info.dev_id] = mapped_device

        return mapped_devices

    def _map_device_connections(self,
                                topology: TopologyModel,
                                mapped_devices: dict[str, MappedDeviceModel]) -> dict[str, MappedDeviceModel]:
        for device_info in topology.topology:
            mapped_devices[device_info.dev_id].neighbours = [
                ConnectionModel(
                    neighbour_name=mapped_devices[neighbour.to_id].name,
                    from_interface=neighbour.from_if,
                    to_interface=neighbour.to_if,
                )
                for neighbour in device_info.dev_neighbours
            ]

        return mapped_devices


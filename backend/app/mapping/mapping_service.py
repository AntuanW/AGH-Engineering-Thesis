from bson.objectid import ObjectId
from fastapi import Depends

from app.models.connection import ConnectionModel
from app.models.mapped_device import MappedDeviceModel
from app.models.mapping import MappingModel
from app.models.rack import RackModel
from app.models.topology import TopologyModel
from app.repository.device_repository import DeviceRepository
from app.repository.lab_group_repository import LabGroupRepository
from app.repository.mapping_repository import MappingRepository
from app.repository.topology_repository import TopologyRepository
from app.models.device import DeviceModel


class MappingService:
    def __init__(self,
                 lab_group_repo: LabGroupRepository = Depends(LabGroupRepository),
                 device_repo: DeviceRepository = Depends(DeviceRepository),
                 topology_repo: TopologyRepository = Depends(TopologyRepository),
                 mapping_repo: MappingRepository = Depends(MappingRepository)):
        self._lab_group_repo = lab_group_repo
        self._device_repo = device_repo
        self._topology_repo = topology_repo
        self._mapping_repo = mapping_repo

    def get_mappings_by_topology_id(self, topology_id: str, group_numbers: list | None = None):
        if group_numbers is None:
            group_numbers = self._lab_group_repo.get_all_group_ids()

        topology = self._topology_repo.find_object({"_id": ObjectId(topology_id)})
        if topology is None:
            raise KeyError(f"No topology with id {topology_id}.")

        mappings = self._mapping_repo.find_objects({"topology_name": topology.name, "lab_group_number": {"$in": group_numbers}})
        if len(mappings) == 0:
            raise KeyError(f"No mappings found. Please generate them first.")
        return mappings

    def get_device_mappings(self, topology_id: str, group_numbers: list[int] | None) -> list[MappingModel]:
        topology_id = ObjectId(topology_id)
        topology = self._topology_repo.find_object({"_id": topology_id})

        if group_numbers is None:
            group_numbers = self._lab_group_repo.get_all_group_ids()

        mapping_list = []
        for group_number in group_numbers:
            mapped_devices = self._get_device_mapping_for_lab_group(topology, group_number)
            mapping_list.append(MappingModel(
                topology_name=topology.name,
                lab_group_number=group_number,
                mapped_devices=mapped_devices
            ))

        for mapping in mapping_list:
            self._mapping_repo.upsert({
                "topology_name": topology.name,
                "lab_group_number": mapping.lab_group_number
            },
            mapping.model_dump())

        return mapping_list

    def _get_device_mapping_for_lab_group(self, topology: TopologyModel, group_number: int) -> list[MappedDeviceModel]:
        group = self._lab_group_repo.find_object({"lab_group_number": group_number})
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
                    origin_name=mapped_devices[device_info.dev_id].name,
                    neighbour_name=mapped_devices[neighbour.to_id].name,
                    from_interface=neighbour.from_if,
                    to_interface=neighbour.to_if,
                )
                for neighbour in device_info.dev_neighbours
            ]

        return mapped_devices

    def get_setup_instructions(self, mapping_list: list[MappingModel]) -> dict[int, str]:
        instructions = {}
        for mapping in mapping_list:
            instructions[mapping.lab_group_number] = self.get_setup_instructions_for_mapping(mapping)
        return instructions

    def get_setup_instructions_for_mapping(self, mapping: MappingModel) -> list[str]:
        instructions = [f"SETUP GUIDE FOR GROUP #{mapping.lab_group_number}"]
        connections = set()
        for mapped_device in mapping.mapped_devices:
            connections.update(mapped_device.neighbours)
        for connection in connections:
            instructions.append(f"Connect {connection.origin_name}:{connection.from_interface} "
                                f"-> {connection.neighbour_name}:{connection.to_interface}")

        ip = self._lab_group_repo.find_object({"lab_group_number": mapping.lab_group_number}).rack.config_port_ip_address
        instructions.append(f"Find config ports with IP {ip}")
        for mapped_device in mapping.mapped_devices:
            instructions.append(f"Connect {mapped_device.name} to config port {mapped_device.port}")
        return instructions



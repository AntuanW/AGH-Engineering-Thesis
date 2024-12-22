from unittest.mock import patch

from app.mapping.mapping_service import MappingService
from app.models.device import Interface
from app.models.topology import TopologyModel
from app.repository.device_repository import DeviceRepository
from app.repository.lab_group_repository import LabGroupRepository
from app.repository.mapping_repository import MappingRepository
from app.repository.topology_repository import TopologyRepository

from bson.objectid import ObjectId

from app.running_config.util.device_config_types import DeviceConfigInfo, DeviceType, DeviceLink


class TestMapping:
    @patch("app.repository.topology_repository.TopologyRepository.find_object")
    def test_mapping(self, find_object_mock):
        mock_topology_id = '5f8f8f8f8f8f8f8f8f8f8f8f'

        mock_topology = TopologyModel(
            name="test",
            topology=[
                DeviceConfigInfo(
                    dev_name="r1",
                    dev_id="r1",
                    dev_type=DeviceType.ROUTER,
                    dev_running_config=[],
                    dev_neighbours=[
                        DeviceLink(
                            from_id="r1", from_if="Fa0/0", to_id="s1", to_if="Fa0/5"
                        ),
                        DeviceLink(
                            from_id="r1", from_if="Fa0/1", to_id="s2", to_if="Fa0/69"
                        ),
                    ]
                ),

                DeviceConfigInfo(
                    dev_name="s1",
                    dev_id="s1",
                    dev_type=DeviceType.SWITCH,
                    dev_running_config=[],
                    dev_neighbours=[
                        DeviceLink(
                            from_id="s1", from_if="Fa0/5", to_id="r1", to_if="Fa0/0"
                        )
                    ]
                ),

                DeviceConfigInfo(
                    dev_name="s2",
                    dev_id="s2",
                    dev_type=DeviceType.SWITCH,
                    dev_running_config=[],
                    dev_neighbours=[
                        DeviceLink(
                            from_id="s2", from_if="Fa0/69", to_id="r1", to_if="Fa0/1"
                        )
                    ]
                ),
            ]
        )

        find_object_mock.return_value = mock_topology

        mapping_service = MappingService(LabGroupRepository(), DeviceRepository(),
                                         TopologyRepository(), MappingRepository())

        mapping = mapping_service.get_device_mappings(mock_topology_id, [5])

        assert mapping[0].mapped_devices[0].device_type == DeviceType.ROUTER
        assert mapping[0].mapped_devices[1].device_type == DeviceType.SWITCH
        assert Interface(mapping[0].mapped_devices[0].neighbours[0].to_interface) == Interface("Fa0/5")
        assert Interface(mapping[0].mapped_devices[0].neighbours[1].to_interface) == Interface("Fa0/1")

    @patch("app.repository.topology_repository.TopologyRepository.find_object")
    def test_pc_mapping(self, find_object_mock):
        mock_topology_id = '5f8f8f8f8f8f8f8f8f8f8f8f'

        mock_topology = TopologyModel(
            name="test",
            topology=[
                DeviceConfigInfo(
                    dev_name="r1",
                    dev_id="r1",
                    dev_type=DeviceType.ROUTER,
                    dev_running_config=[],
                    dev_neighbours=[
                        DeviceLink(
                            from_id="r1", from_if="Fa0/0", to_id="K11", to_if="Fa0"
                        ),
                    ]
                ),

                DeviceConfigInfo(
                    dev_name="K11",
                    dev_id="K11",
                    dev_type=DeviceType.PC,
                    dev_running_config=[],
                    dev_neighbours=[
                        DeviceLink(
                            from_id="K11", from_if="Fa0", to_id="r1", to_if="Fa0/0"
                        )
                    ]
                ),
            ]
        )

        find_object_mock.return_value = mock_topology

        service = MappingService(LabGroupRepository(), DeviceRepository(), TopologyRepository(), MappingRepository())
        mappings = service.get_device_mappings(mock_topology_id, [5])

        assert mappings[0].mapped_devices[1].device_type == DeviceType.PC
        assert mappings[0].mapped_devices[0].neighbours[0].to_interface == "PC0"
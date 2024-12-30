from collections import defaultdict
from unittest.mock import patch

from app.common.netmiko.netmiko_device import NetmikoDevice
from app.common.netmiko.netmiko_device_type import NetmikoDeviceType
from app.config_download.config_download_service import ConfigDownloadService
from app.config_download.utils.download_config_request import DownloadConfigRequest
from app.config_download.utils.downloaded_config import DownloadedConfig
import unittest
from app.mapping.mapping_service import MappingService
from app.models.connection import ConnectionModel
from app.models.device import Interface
from app.models.mapped_device import MappedDeviceModel
from app.models.mapping import MappingCollectionModel, MappingType
from app.models.topology import TopologyModel
from app.repository.device_repository import DeviceRepository
from app.repository.lab_group_repository import LabGroupRepository
from app.repository.mapping_repository import MappingRepository
from app.repository.topology_repository import TopologyRepository
from app.running_config.util.device_config_types import DeviceConfigInfo, DeviceType, DeviceLink


class TestMapping(unittest.TestCase):
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

        assert mapping.mappings[5][0].device_type == DeviceType.ROUTER
        assert mapping.mappings[5][1].device_type == DeviceType.SWITCH
        assert Interface(mapping.mappings[5][0].neighbours[0].to_interface) == Interface("Fa0/5")
        assert Interface(mapping.mappings[5][0].neighbours[1].to_interface) == Interface("Fa0/1")

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
        mapping = service.get_device_mappings(mock_topology_id, [5])

        assert mapping.mappings[5][1].device_type == DeviceType.PC
        assert mapping.mappings[5][0].neighbours[0].to_interface == "PC0"

    def test_model(self):
        model = MappingCollectionModel(name="adwd", type=MappingType.CREATED_FROM_PKT, topology_id="asdawd",
                                       mappings=defaultdict(list, {
                                           2: [MappedDeviceModel(
                                                name="adw",
                                                ip_address="123123",
                                                port=123151,
                                                device_type=DeviceType.ROUTER,
                                                netmiko_device_type=NetmikoDeviceType.CISCO_IOS,
                                                mapped_config=[],
                                                neighbours=[]
                                            )]
                                       }))

        assert model.mappings[2][0].name == "adw"

        dict_ = model.model_dump()

        model2 = MappingCollectionModel(**dict_)

        assert model2.mappings[2][0].name == "adw"
        assert type(tuple(model2.mappings.keys())[0]) == int

    def test_mapping_from_downloaded_config(self):
        import random

        devices = [
            NetmikoDevice(name="r1", ip_address="xxx", port=1000),
            NetmikoDevice(name="r2", ip_address="yyy", port=2000)
        ]

        guid = hex(random.getrandbits(16))
        dcr = DownloadConfigRequest(lab_name=f"test-{guid}", lab_group=1, devices=devices)
        dcr2 = DownloadConfigRequest(lab_name=f"test-{guid}", lab_group=2, devices=devices)
        dc = [
            DownloadedConfig(name="r1", device_type=DeviceType.ROUTER, neighbours=[
                ConnectionModel(origin_name="r1", neighbour_name="r2", from_interface="Fa0/0", to_interface="Fa0/1"),
            ], config="aaa\nbbb\n"),
            DownloadedConfig(name="r2", device_type=DeviceType.ROUTER, neighbours=[
                ConnectionModel(origin_name="r2", neighbour_name="r1", from_interface="Fa0/1", to_interface="Fa0/0"),
            ], config="ccc\nddd\n")
        ]

        service = MappingService(LabGroupRepository(), DeviceRepository(),
                                 TopologyRepository(), MappingRepository(), ConfigDownloadService())
        mcm = service.upsert_mapping_from_downloaded_config(dcr, dc)
        mcm2 = service.upsert_mapping_from_downloaded_config(dcr2, dc)

        assert mcm2.mappings[2][0].mapped_config == ['aaa', 'bbb', '']

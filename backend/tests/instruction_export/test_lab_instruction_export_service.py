import unittest
from unittest.mock import patch, MagicMock

from bson.objectid import ObjectId

from app.models.mapped_device import MappedDeviceModel
from app.models.mapping import MappingCollectionModel, MappingType
from app.models.topology import TopologyModel
from app.repository.lab_group_repository import LabGroupRepository
from app.repository.topology_repository import TopologyRepository
from app.running_config.util.device_config_types import DeviceType
from app.common.netmiko.netmiko_device_type import NetmikoDeviceType
from app.instruction_export.lab_instruction_export_service import LabInstructionExportService


class TestLabInstructionExportService(unittest.TestCase):
    @patch("app.repository.topology_repository.TopologyRepository.find_object")
    def test_export_instructions(self, find_object_mock):
        mock_lab_group_number = 1
        mock_mapping_id = ObjectId('5f8f8f8f8f8f8f8f8f8f8f8f')
        mock_topology_id = '5f8f8f8f8f8f8f8f8f8f8f8f'
        mock_mapped_device = MappedDeviceModel(
            name='Router',
            ip_address='0.0.0.0',
            port=2001,
            device_type=DeviceType.ROUTER,
            netmiko_device_type=NetmikoDeviceType.CISCO_IOS,
            mapped_config=[],
            neighbours=[]
        )
        mock_mapping_collection = {
            '_id': mock_mapping_id,
            'name': "test",
            'type': MappingType.CREATED_FROM_PKT,
            'topology_id': mock_topology_id,
            'mappings': {
                1: [mock_mapped_device]
            }
        }

        mock_topology = TopologyModel(
            name="test",
            topology=[]
        )

        find_object_mock.return_value = mock_topology

        pdf_generator_mock = MagicMock()
        pdf_generator_mock.generate_pdf.return_value = ""
        pdf_generator_mock.filename.return_value = "test"

        mapping_collection = MappingCollectionModel(**mock_mapping_collection)
        lab_instruction_export_service = LabInstructionExportService(TopologyRepository(), LabGroupRepository(), pdf_generator_mock)
        filename = lab_instruction_export_service.export_instructions(mapping_collection)
        self.assertTrue(filename)

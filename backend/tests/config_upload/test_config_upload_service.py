import unittest
from unittest.mock import MagicMock, patch

from app.config_upload.config_upload_service import ConfigUploadService
from app.repository.mapping_repository import MappingRepository
from app.models.mapped_device import MappedDeviceModel
from app.running_config.util.device_config_types import DeviceType
from app.common.netmiko.netmiko_device_type import NetmikoDeviceType


class TestConfigUploadService(unittest.TestCase):
    @patch("app.common.netmiko.netmiko_client.NetmikoClient")
    def test_build_netmiko_devices(self, netmiko_client_mock):
        mock_lab_group_number = 1
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
        mock_mapping = {
            'lab_group_number': mock_lab_group_number,
            'topology_id': mock_topology_id,
            'mapped_devices': [mock_mapped_device]
        }

        mapping_repository = MappingRepository()
        mapping_repository.find_devices_by_group = MagicMock(return_value=mock_mapping['mapped_devices'])
        mapped_devices = mapping_repository.find_devices_by_group(mock_lab_group_number, mock_topology_id)

        config_upload_service = ConfigUploadService(netmiko_client_mock)
        config_upload_service.upload_configs(mapped_devices)
        netmiko_client_mock.upload_config_to_device.assert_called_once()



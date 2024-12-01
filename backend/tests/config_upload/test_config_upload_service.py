import unittest

from app.config_upload.config_upload_service import ConfigUploadService
from app.config_upload.util.netmiko_device import NetmikoDevice
from app.repository.mapping_repository import MappingRepository


class TestConfigUploadService(unittest.TestCase):
    def test_build_netmiko_devices(self):
        lab_group_number = 1
        mapping_repository = MappingRepository()
        mapped_devices = mapping_repository.find_devices_by_group(lab_group_number)

        config_upload_service = ConfigUploadService()
        netmiko_devices = config_upload_service.build_netmiko_devices(mapped_devices)

        assert len(netmiko_devices) == 3, f"Expected 3 devices, got {len(netmiko_devices)}"
        assert isinstance(netmiko_devices[0], NetmikoDevice), f"Expected NetmikoDevice, got {type(netmiko_devices[0])}"

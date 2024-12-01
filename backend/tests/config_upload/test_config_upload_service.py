import unittest
from bson.objectid import ObjectId

from app.config_upload.config_upload_service import ConfigUploadService
from app.repository.topology_repository import TopologyRepository

class TestConfigUploadService(unittest.TestCase):
    def test_build_netmiko_devices(self):
        topology_repository = TopologyRepository()
        topology_id = ObjectId('671e6c7c15f4350cff3d7770')
        topology = topology_repository.find_by_id(topology_id)

        config_upload_service = ConfigUploadService()
        devices = config_upload_service.build_netmiko_devices(topology)
        assert len(devices) == 9, f"Expected 9 devices, got {len(devices)}"
        assert len(devices[0].config) == 31, f"Expected 31 commands, got {len(devices[0].config)}"

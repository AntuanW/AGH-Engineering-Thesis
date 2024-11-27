from app.mapping.mapping_service import MappingService
from app.repository.device_repository import DeviceRepository
from app.repository.lab_group_repository import LabGroupRepository
from app.repository.topology_repository import TopologyRepository

from pprint import pp

class TestMapping:
    def test_mapping(self):
        topology_id = "6740801f1b9237fa343ad93b"

        service = MappingService(LabGroupRepository(), DeviceRepository(), TopologyRepository())
        mappings = service.get_device_mappings(topology_id, [1, 2])

        print()
        for group_mapping in mappings:
            for mapped_device in group_mapping.mapped_devices:
                mapped_device.mapped_config = []
                pp(mapped_device.__dict__)



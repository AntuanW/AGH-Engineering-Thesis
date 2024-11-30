from app.mapping.mapping_service import MappingService
from app.repository.device_repository import DeviceRepository
from app.repository.lab_group_repository import LabGroupRepository
from app.repository.mapping_repository import MappingRepository
from app.repository.topology_repository import TopologyRepository

from pprint import pp

class TestMapping:
    def test_mapping(self):
        topology_id = "6740801f1b9237fa343ad93b"

        service = MappingService(LabGroupRepository(), DeviceRepository(), TopologyRepository(), MappingRepository())
        mappings = service.get_device_mappings(topology_id, [1, 2])

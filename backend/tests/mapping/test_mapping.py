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
        # basic_mappings = service.get_device_mappings(topology_id, [1, 2])
        #
        # topology_id = "6750ddc5d004fe4bf37b2380"
        # gi_switch_mappings = service.get_device_mappings(topology_id, [1, 2])

        topology_id = "6750df73d004fe4bf37b2383"
        gi_3x_switch_mappings = service.get_device_mappings(topology_id, [1])
        print(gi_3x_switch_mappings)
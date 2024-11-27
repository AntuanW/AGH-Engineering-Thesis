
from app.mapping.mapping_service import MappingService
from app.repository.decrypted_xml_repository import DecryptedXMLRepository
from app.repository.device_repository import DeviceRepository
from app.repository.lab_group_repository import LabGroupRepository
from app.repository.topology_repository import TopologyRepository


class TestMapping:
    def test_mapping(self):
        topology_id = "6740801f1b9237fa343ad93b"

        service = MappingService(LabGroupRepository(), DeviceRepository(), TopologyRepository())
        mapping = service.get_device_mapping(topology_id, [1])
        print(mapping)

    def test_base_repo_generic(self):
        dev_repo = DecryptedXMLRepository()
        # dev = DeviceModel(**dev_repo.find_one({}))
        dev = dev_repo.find_one({})
        print(dev)

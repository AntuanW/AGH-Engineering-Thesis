from fastapi import Depends

from app.repository.decrypted_xml_repository import DecryptedXMLRepository
from app.repository.lab_group_repository import LabGroupRepository
from app.repository.mapping_repository import MappingRepository
from app.repository.topology_repository import TopologyRepository


class DTOService:
    def __init__(self,
        xml_repo: DecryptedXMLRepository = Depends(DecryptedXMLRepository),
        topo_repo: TopologyRepository = Depends(TopologyRepository),
        group_repo: LabGroupRepository = Depends(LabGroupRepository),
        mapping_repo: MappingRepository = Depends(MappingRepository)
                 ):
        self.xml_repo = xml_repo
        self.topo_repo = topo_repo
        self.group_repo = group_repo
        self.mapping_repo = mapping_repo

    def _list_mapping_names(self):
        """
        Retrieves {name, id} of topologies, for which a mapping exists
        """
        mapping_topo_ids = self.mapping_repo.find_topology_ids()
        topologies_with_mappings = list(self.topo_repo.find(
            {"_id": {"$in": mapping_topo_ids}}, {"name": 1}))
        return [{"name": obj["name"], "_id": str(obj["_id"])} for obj in topologies_with_mappings]

    def create_index_dto(self):
        return {
            "XMLs": self.xml_repo.list_names(),
            "topologies": self.topo_repo.list_names(),
            "groups": self.group_repo.get_all_groups(),
            "mappings": self.mapping_repo.list_names()
        }


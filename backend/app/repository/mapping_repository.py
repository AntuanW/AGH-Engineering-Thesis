from .base_repository import BaseRepository
from pymongo.collection import Collection

from ..models.mapped_device import MappedDeviceModel
from ..models.mapping import MappingCollectionModel
from bson import ObjectId


class MappingRepository(BaseRepository[MappingCollectionModel]):
    def get_collection(self) -> Collection:
        return self.db.get_collection('mappings')

    def insert(self, mapping: MappingCollectionModel):
        return super().insert(mapping.model_dump())

    def find_topology_ids(self):
        """
        Returns topology IDs for which a mapping exists
        """
        return [ObjectId(x["topology_id"]) for x in self.get_collection().find(
            {}, {"topology_id": 1, "_id": 0})]

    def find_mapped_devices_by_topology_id(self, topology_id: str) -> dict[int, list[MappedDeviceModel]]:
        mapping_collection: MappingCollectionModel = self.find_object({'topology_id': topology_id}) or {}
        return mapping_collection.mappings

    def find_mapped_devices_by_mapping_name(self, mapping_name: str) -> dict[int, list[MappedDeviceModel]]:
        """
        Finds a mapping object by its name. Mappings created by downloading configurations do not have
        corresponding topologies.
        """
        mapping_collection: MappingCollectionModel = self.find_object({'name': mapping_name}) or {}
        return mapping_collection.mappings

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

    def find_devices_by_group(self, lab_group_number: int, topology_id: str) -> dict[int, list[MappedDeviceModel]]:
        mapping_collection: MappingCollectionModel = self.find_object({'lab_group_number': lab_group_number, 'topology_id': topology_id})
        if not mapping_collection:
            return {}
        devices = mapping_collection.mappings
        return devices

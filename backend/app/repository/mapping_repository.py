from .base_repository import BaseRepository
from pymongo.collection import Collection
from ..models.mapping import MappingModel
from bson import ObjectId


class MappingRepository(BaseRepository[MappingModel]):
    def get_collection(self) -> Collection:
        return self.db.get_collection('mappings')

    def insert(self, mapping: MappingModel):
        return super().insert(mapping.model_dump())

    def find_topology_ids(self):
        return [ObjectId(x["topology_id"]) for x in self.get_collection().find(
            {}, {"topology_id": 1, "_id": 0})]

    def find_devices_by_group(self, lab_group_number: int, topology_id: str):
        mapping: MappingModel = self.find_object({'lab_group_number': lab_group_number, 'topology_id': topology_id})
        if not mapping:
            return []
        devices = mapping.mapped_devices
        return devices

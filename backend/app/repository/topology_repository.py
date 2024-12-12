from bson.objectid import ObjectId

from .base_repository import BaseRepository
from ..models.topology import TopologyModel
from app.running_config.util.device_config_types import DeviceConfigInfo


class TopologyRepository(BaseRepository[TopologyModel]):
    def get_collection(self):
        return self.db['topology']

    def insert(self, topology: TopologyModel):
        return super().insert(topology.model_dump())

    def list_names(self):
        return [{"name": obj["name"], "_id": str(obj["_id"])}
            for obj in self.get_collection().find({}, {"name": 1})]

    def find_by_id(self, topology_id: ObjectId) -> list[DeviceConfigInfo]:
        topology_dict: dict = super().find_one({"_id": topology_id})
        if not topology_dict:
            return []
        return [DeviceConfigInfo(**device) for device in topology_dict['topology']]

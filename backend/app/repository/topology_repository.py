from .base_repository import BaseRepository
from ..models.topology import TopologyModel


class TopologyRepository(BaseRepository[TopologyModel]):
    def get_collection(self):
        return self.db['topology']

    def insert(self, topology: TopologyModel):
        return super().insert(topology.model_dump())

from .base_repository import BaseRepository
from ..models.connection import ConnectionModel


class ConnectionRepository(BaseRepository):
    def get_collection(self):
        return self.db['connections']

    def insert(self, connection: ConnectionModel):
        return super().insert(connection.model_dump())

    def find_all(self) -> list[ConnectionModel] | None:
        connections = self.find({})
        return [ConnectionModel(**connection.get('connection', {})) for connection in
                connections]

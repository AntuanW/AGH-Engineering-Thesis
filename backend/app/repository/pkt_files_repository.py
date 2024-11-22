from .base_repository import BaseRepository
from pymongo.collection import Collection


class PktFilesRepository(BaseRepository):

    def get_collection(self) -> Collection:
        return self.db.get_collection('pkt_files')

    def insert(self, document):
        return super().insert(document)
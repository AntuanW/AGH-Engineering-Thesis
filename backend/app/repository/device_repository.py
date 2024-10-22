from .base_repository import BaseRepository

class DeviceRepository(BaseRepository):

    def get_collection(self):
        return self.db['devices']

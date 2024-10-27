from .base_repository import BaseRepository
from ..models.device import DeviceModel


class DeviceRepository(BaseRepository):

    def get_collection(self):
        return self.db['devices']

    def insert(self, device: DeviceModel):
        return super().insert(device.model_dump())

from .base_repository import BaseRepository
from ..models.device import DeviceModel
from pymongo.collection import Collection


class DeviceRepository(BaseRepository):

    def get_collection(self) -> Collection:
        return self.db.get_collection('devices')

    def insert(self, device: DeviceModel):
        return super().insert(device.model_dump())

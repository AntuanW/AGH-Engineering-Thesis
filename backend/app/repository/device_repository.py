from bson import ObjectId

from .base_repository import BaseRepository
from ..models.device import DeviceModel
from pymongo.collection import Collection


class DeviceRepository(BaseRepository):

    def get_collection(self) -> Collection:
        return self.db.get_collection('devices')

    def insert(self, device: DeviceModel):
        return super().insert(device.model_dump())

    def find_by_id(self, device_id: ObjectId) -> DeviceModel | None:
        device_dict: dict = self.find_one({'_id': device_id})
        print(device_dict)
        if not device_dict:
            return None
        return DeviceModel(**device_dict)
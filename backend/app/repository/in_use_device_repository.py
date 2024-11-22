from .base_repository import BaseRepository
from ..models.in_use_device import InUseDeviceModel


class InUseDeviceRepository(BaseRepository):
    def get_collection(self):
        return self.db['in_use_device']

    def insert(self, in_use_device: InUseDeviceModel):
        return super().insert(in_use_device.model_dump())
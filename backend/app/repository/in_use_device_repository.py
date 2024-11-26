from .base_repository import BaseRepository
from ..models.in_use_device import InUseDeviceModel


class InUseDeviceRepository(BaseRepository):
    def get_collection(self):
        return self.db['in_use_devices']

    def insert(self, in_use_device: InUseDeviceModel):
        return super().insert(in_use_device.model_dump())

    def find_all(self) -> list[InUseDeviceModel] | None:
        in_use_devices = self.find({})
        return [InUseDeviceModel(**in_use_device.get('in_use_device', {})) for in_use_device in
                in_use_devices]


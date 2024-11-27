from .base_repository import BaseRepository
from pymongo.collection import Collection
from ..models.mapping import MappingModel
from ..models.mapped_device import MappedDeviceModel
from pydantic.networks import IPvAnyAddress
from ..models.connection import ConnectionModel
from ..config_upload.util.netmiko_types import NetmikoDeviceType


class MappingRepository(BaseRepository):

    def get_collection(self) -> Collection:
        return self.db.get_collection('mappings')

    def insert(self, mapping: MappingModel):
        return super().insert(mapping.model_dump())

    def find_devices_by_group(self, lab_group: int):
        mapping: dict = self.find_one({'group': lab_group})
        if not mapping:
            return []
        mapped_devices = mapping.get('mapped_devices')
        devices = []
        for device in mapped_devices:
            d = MappedDeviceModel(
                name=device.get('name'),
                netmiko_device_type=NetmikoDeviceType(device.get('netmiko_device_type')),
                ip_address=IPvAnyAddress(device.get('ip_address')),
                port=device.get('port'),
                neighbours=[ConnectionModel(**n) for n in device.get('neighbours')],
                mapped_config=device.get('mapped_config'))
            devices.append(d)
        return devices

    def find_all(self):
        mappings = self.find({})
        if not mappings:
            return []
        result = []
        for mapping in mappings:
            lab_group = mapping.get('lab_group')
            devices = self.find_devices_by_group(lab_group)
            result.append(MappingModel(lab_group=lab_group, mapped_devices=devices))
        return result

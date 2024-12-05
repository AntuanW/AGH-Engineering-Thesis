from .base_repository import BaseRepository
from pymongo.collection import Collection
from ..models.mapping import MappingModel
from ..models.mapped_device import MappedDeviceModel
from pydantic.networks import IPvAnyAddress
from ..models.connection import ConnectionModel
from ..config_upload.util.netmiko_types import NetmikoDeviceType

from bson.objectid import ObjectId


class MappingRepository(BaseRepository[MappingModel]):

    def get_collection(self) -> Collection:
        return self.db.get_collection('mappings')

    def insert(self, mapping: MappingModel):
        return super().insert(mapping.model_dump())

    def find_devices_by_group(self, topology_id: str, lab_group_number: int):
        mapping: MappingModel = self.find_object({'topology_id': topology_id, 'lab_group_number': lab_group_number})
        if not mapping:
            return []
        devices = mapping.mapped_devices
        return devices

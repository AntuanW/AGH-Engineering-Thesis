from pydantic import BaseModel
from .mapped_device import MappedDeviceModel


class MappingModel(BaseModel):
    lab_group_number: int
    topology_id: str
    mapped_devices: list[MappedDeviceModel]

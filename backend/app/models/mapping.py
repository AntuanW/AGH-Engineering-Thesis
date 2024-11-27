from pydantic import BaseModel
from .mapped_device import MappedDeviceModel


class MappingModel(BaseModel):
    lab_group: int
    mapped_devices: list[MappedDeviceModel]

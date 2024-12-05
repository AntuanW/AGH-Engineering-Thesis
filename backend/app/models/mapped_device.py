from pydantic import BaseModel
from .device import DeviceType
from .connection import ConnectionModel
from ..config_upload.util.netmiko_types import NetmikoDeviceType


class MappedDeviceModel(BaseModel):
    name: str
    device_type: DeviceType
    netmiko_device_type: NetmikoDeviceType
    ip_address: str
    port: int
    neighbours: list[ConnectionModel]
    mapped_config: list[str]

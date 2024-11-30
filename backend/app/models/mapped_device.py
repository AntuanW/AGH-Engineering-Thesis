from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress
from .connection import ConnectionModel
from ..config_upload.util.netmiko_types import NetmikoDeviceType


class MappedDeviceModel(BaseModel):
    name: str
    netmiko_device_type: NetmikoDeviceType
    ip_address: str
    port: int
    neighbours: list[ConnectionModel]
    mapped_config: list[str]

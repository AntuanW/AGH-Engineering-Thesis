from pydantic import BaseModel
from .rack import RackModel
from ..running_config.util.device_config_types import DeviceType
from ..config_upload.util.netmiko_types import NetmikoDeviceType


class DeviceModel(BaseModel):
    name: str
    device_type: DeviceType
    netmiko_device_type: NetmikoDeviceType
    rack: RackModel
    interfaces: list[str]
    commands: list[str]

from pydantic import BaseModel
from enum import Enum

from app.config_upload.util.netmiko_types import NetmikoDeviceType


class DeviceType(str, Enum):
    ROUTER = 'ROUTER'
    SWITCH = 'SWITCH'
    PC = 'PC'
    UNKNOWN = 'UNKNOWN'

    def to_netmiko_device_type(self):
        return NetmikoDeviceType.CISCO_IOS if self.value != self.UNKNOWN else NetmikoDeviceType.UNKNOWN


class DeviceLink(BaseModel):
    from_id: str
    from_iface: str
    to_id: str
    to_iface: str


class DeviceConfigInfo(BaseModel):
    dev_id: str
    dev_type: DeviceType
    dev_running_config: list[str]
    dev_name: str
    dev_neighbours: list[DeviceLink]

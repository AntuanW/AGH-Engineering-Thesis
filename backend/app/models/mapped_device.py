from .device import DeviceType
from .connection import ConnectionModel
from app.common.netmiko.netmiko_device_type import NetmikoDeviceType
from ..common.netmiko.netmiko_device import NetmikoDevice


class MappedDeviceModel(NetmikoDevice):
    device_type: DeviceType
    netmiko_device_type: NetmikoDeviceType
    neighbours: list[ConnectionModel]
    mapped_config: list[str]

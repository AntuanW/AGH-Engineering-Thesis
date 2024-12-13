from ..models.mapped_device import MappedDeviceModel
from app.common.netmiko.netmiko_client import NetmikoClient
from fastapi import Depends

from ..running_config.util.device_config_types import DeviceType


class ConfigUploadService:
    def __init__(self, netmiko_client: NetmikoClient = Depends(NetmikoClient)):
        self.netmiko_client = netmiko_client

    def upload_configs(self, devices: list[MappedDeviceModel]):
        for device in devices:
            self._upload(device)

    def _upload(self, device: MappedDeviceModel):
        if device.device_type == DeviceType.SWITCH or device.device_type == DeviceType.ROUTER:
            self.netmiko_client.upload_config_to_device(device)

from ..models.mapped_device import MappedDeviceModel
from app.common.netmiko.netmiko_client import NetmikoClient
from fastapi import Depends


class ConfigUploadService:
    def __init__(self, netmiko_client: NetmikoClient = Depends(NetmikoClient)):
        self.netmiko_client = netmiko_client

    def upload_configs(self, devices: list[MappedDeviceModel]):
        for device in devices:
            self.netmiko_client.upload_config_to_device(device)

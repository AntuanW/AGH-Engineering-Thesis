import time
import re

from fastapi import Depends
from app.common.netmiko.netmiko_client import NetmikoClient
from .utils.download_config_request import DownloadConfigRequest
from .utils.downloaded_config import DownloadedConfig
from app.common.netmiko.netmiko_device import NetmikoDevice
from ..models.connection import ConnectionModel
from ..running_config.util.device_config_types import DeviceType


class ConfigDownloadService:
    def __init__(self, netmiko_client: NetmikoClient = Depends(NetmikoClient)):
        self.netmiko_client = netmiko_client

    def change_hostnames_and_cdp_timers(self, devices: list[NetmikoDevice]):
        for device in devices:
            self.netmiko_client.set_hostname_and_cdp_timers(device)
        time.sleep(10)

    def download_devices_config(self, download_config_request: DownloadConfigRequest) -> list[DownloadedConfig]:
        download_results = []
        for device in download_config_request.devices:
            config, neighbors = self.netmiko_client.download_config_from_device(device)

            download_results.append(DownloadedConfig(
                name=device.name,
                device_type=self._get_device_type(device),
                neighbours=self._parse_neighbors(neighbors, device.name),
                config=config
            ))
        return download_results

    def _parse_neighbors(self, neighbors_string: str, origin_name: str) -> list[ConnectionModel]:
        connections = []
        split_regex = r"\s{2,}"
        split_neighbors = neighbors_string.split("\n")[3:-1]
        for record in split_neighbors:
            # returns list of lists where elements are: Device ID, Local Intrfce, Holdtime, Capability, Platform, Port ID
            neighbor = re.split(split_regex, record)

            connections.append(ConnectionModel(
                origin_name=origin_name,
                neighbour_name=neighbor[0],
                from_interface=neighbor[1],
                to_interface=neighbor[5],
            ))
        return connections

    def _get_device_type(self, device: NetmikoDevice):
        return DeviceType.SWITCH if device.name.startswith("S") else DeviceType.ROUTER

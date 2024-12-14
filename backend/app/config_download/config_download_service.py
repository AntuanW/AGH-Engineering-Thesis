import time
import re
import logging

from fastapi import Depends
from app.common.netmiko.netmiko_client import NetmikoClient
from .utils.download_config_request import DownloadConfigRequest
from .utils.downloaded_config import DownloadedConfig
from .exceptions.config_download_exceptions import EmptyDownloadException
from app.common.netmiko.netmiko_device import NetmikoDevice
from ..models.connection import ConnectionModel
from ..running_config.util.device_config_types import DeviceType


class ConfigDownloadService:
    def __init__(self, netmiko_client: NetmikoClient = Depends(NetmikoClient)):
        self.netmiko_client = netmiko_client

    def change_hostnames_and_cdp_timers(self, devices: list[NetmikoDevice]):
        for device in devices:
            logging.info(f"Setting hostname and timers for {device.name}")
            self.netmiko_client.set_hostname_and_cdp_timers(device)
        time.sleep(10)

    def download_devices_config(self, download_config_request: DownloadConfigRequest) -> list[DownloadedConfig]:
        download_results = []
        for device in download_config_request.devices:
            logging.info(f"Downloading config for {device.name}")
            config, neighbors = self._download(device)

            if not (config or neighbors):
                raise EmptyDownloadException("Something went wrong with config download.")

            download_results.append(DownloadedConfig(
                name=device.name,
                device_type=self._get_device_type(device),
                neighbours=self._parse_neighbors(neighbors, device.name),
                config=config
            ))
            logging.info(f"Finished downloading config for {device.name} successfully.")
        return download_results

    def _download(self, device: NetmikoDevice):
        if device.device_type == DeviceType.SWITCH or device.device_type == DeviceType.ROUTER:
            return self.netmiko_client.download_config_from_device(device)
        return "", ""

    def _parse_neighbors(self, neighbors_string: str, origin_name: str) -> list[ConnectionModel]:
        cdp_neighbors = []
        dev_regex = r"^(S\d{2}|R\d{2})"
        whitespace_regex = r"\s{2,}"

        logging.info(f"Parsing {origin_name} neighbors")
        for line in neighbors_string.splitlines():
            if re.match(dev_regex, line):
                split_line = re.split(whitespace_regex, line)
                cdp_neighbors.append((
                    split_line[0],
                    split_line[1],
                    self._get_remote_interface(split_line[4])
                ))

        connections = []
        for device_id, local_interface, remote_interface in cdp_neighbors:
            connections.append(ConnectionModel(
                origin_name=origin_name,
                neighbour_name=device_id,
                from_interface=local_interface,
                to_interface=remote_interface
            ))
        return connections

    def _get_device_type(self, device: NetmikoDevice):
        switch_regex = r"^S\d{2}"
        router_regex = r"^R\d{2}"

        if re.match(switch_regex, device.name):
            return DeviceType.SWITCH

        if re.match(router_regex, device.name):
            return DeviceType.ROUTER

        return DeviceType.UNKNOWN

    def _get_remote_interface(self, line: str):
        return line.split(" ", 1)[1]

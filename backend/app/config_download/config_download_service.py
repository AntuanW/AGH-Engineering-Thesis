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

    def change_cdp_timers(self, devices: list[NetmikoDevice]):
        for device in devices:
            logging.info(f"Setting timers for {device.port}")
            self.netmiko_client.set_cdp_timers(device)
        time.sleep(10)

    def download_devices_config(self, download_config_request: DownloadConfigRequest) -> list[DownloadedConfig]:
        download_results = []
        for device in download_config_request.devices:
            logging.info(f"Downloading config for {device.port}")
            config, neighbors, hostname, device_type_str = self.netmiko_client.download_config_from_device(device)

            if not (config and neighbors):
                raise EmptyDownloadException("Something went wrong with config download.")

            download_results.append(DownloadedConfig(
                name=hostname,
                device_type=self._get_device_type(device_type_str),
                neighbours=self._parse_neighbors(neighbors, hostname),
                config=config
            ))
            logging.info(f"Finished downloading config for {device.port} successfully.")
        return download_results

    def _parse_neighbors(self, neighbors_string: str, origin_name: str) -> list[ConnectionModel]:
        cdp_neighbors = []
        dev_id = r"^Device ID"
        whitespace_regex = r"\s{2,}"
        merged_last_two_columns_regex = r"^.+\s{1}.+$"
        split_string = neighbors_string.splitlines()
        logging.info(f"Parsing {origin_name} neighbors")
        i = 0
        while not re.match(dev_id, split_string[i]):
            i += 1
        i += 1
        while i < len(split_string) and split_string[i] != "":
            split_line = re.split(whitespace_regex, split_string[i])
            if re.match(merged_last_two_columns_regex, split_line[4]):
                remote_interface = self._get_remote_interface(split_line[4])
            else:
                remote_interface = split_line[5]

            cdp_neighbors.append((
                split_line[0],
                split_line[1],
                remote_interface
            ))
            i+=1

        connections = []
        for device_id, local_interface, remote_interface in cdp_neighbors:
            connections.append(ConnectionModel(
                origin_name=origin_name,
                neighbour_name=device_id,
                from_interface=local_interface,
                to_interface=remote_interface
            ))
        return connections

    def _get_device_type(self, device_type_str: str):
        device_type_str = device_type_str.lower()

        if device_type_str.find("router") >= 0:
            return DeviceType.ROUTER

        if device_type_str.find("switch"):
            return DeviceType.SWITCH

        return DeviceType.UNKNOWN

    def _get_remote_interface(self, line: str):
        return line.split(" ", 1)[1]

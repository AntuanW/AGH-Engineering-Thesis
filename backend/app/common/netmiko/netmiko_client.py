import netmiko
from netmiko import BaseConnection, ConnectHandler
from fastapi import Depends
import time
import logging

from .config import DEVICE_USERNAME, DEVICE_PASSWORD
from .netmiko_constants import NetmikoConstants
from app.models.mapped_device import MappedDeviceModel
from .netmiko_action import NetmikoAction
from .netmiko_device import NetmikoDevice


class NetmikoClient:
    MODE_DIRECT = "cisco_ios"
    CONN_MODE = "generic_termserver_telnet"
    GLOBAL_DELAY_FACTOR_VALUE = 3.0
    RUNNING_CONFIG_CMD = "show running-config"
    CDP_NEIGHBORS_CMD = "show cdp neighbors"
    CDP_TIMER = "cdp timer {}"
    CDP_HOLDTIME = "cdp holdtime {}"
    SHOW_VERSION = "show version"

    def __init__(self, netmiko_constants: NetmikoConstants = Depends(NetmikoConstants)):
        self.netmiko_constants = netmiko_constants

    def upload_config_to_device(self, device: MappedDeviceModel):
        logging.info(f"Uploading config to device {device.name}")
        self._exec_netmiko_action(device, NetmikoAction.UPLOAD_COMMAND_SET)

    def download_config_from_device(self, device: NetmikoDevice) -> tuple[str, str, str, str]:
        running_config, neighbors_str, hostname, device_type  = self._exec_netmiko_action(
            device, NetmikoAction.DOWNLOAD_RUNNING_CONFIG
        )
        return running_config, neighbors_str, hostname, device_type

    def set_cdp_timers(self, device: NetmikoDevice):
        self._exec_netmiko_action(device, NetmikoAction.SET_CDP_TIMERS)

    def _exec_netmiko_action(self, device: NetmikoDevice | MappedDeviceModel, action: NetmikoAction):
        connect_handler: BaseConnection = self._get_connection_handler(
            device.ip_address, device.port, DEVICE_USERNAME, DEVICE_PASSWORD
        )

        with connect_handler:
            connect_handler.establish_connection()
            time.sleep(1)
            connect_handler.write_channel("\r")
            read_channel: str = connect_handler.read_channel()
            if read_channel.find("[yes/no]"):
                connect_handler.write_channel("no\r")
            else:
                connect_handler.write_channel("\r")
            time.sleep(1)
            connect_handler.write_channel("\r")
            time.sleep(1)
            connect_handler.write_channel("\r")
            netmiko.redispatch(connect_handler, device_type=self.MODE_DIRECT)

            for _ in range(5):
                try:
                    connect_handler.enable()
                except Exception:
                    pass

            match action:
                case NetmikoAction.DOWNLOAD_RUNNING_CONFIG:
                    result = self._exec_download_commands(connect_handler)
                case NetmikoAction.UPLOAD_COMMAND_SET:
                    result = self._exec_upload_command(connect_handler, device.mapped_config)
                case NetmikoAction.SET_CDP_TIMERS:
                    result = self._exec_hostname_and_cdp_commands(connect_handler)

        return result

    def _get_connection_handler(self, ip: str, port: int, uname: str, pwd: str) -> BaseConnection:
        handler_dict: dict = self._build_connection_dict(ip, port, uname, pwd)
        return ConnectHandler(**handler_dict)

    def _build_connection_dict(self, ip: str, port: int, uname: str, pwd: str) -> dict:
        return {
            self.netmiko_constants.IP: ip,
            self.netmiko_constants.PORT: port,
            self.netmiko_constants.USERNAME: uname,
            self.netmiko_constants.PASSWORD: pwd,
            self.netmiko_constants.DEVICE_TYPE: self.CONN_MODE,
            self.netmiko_constants.GLOBAL_DELAY_FACTOR: self.GLOBAL_DELAY_FACTOR_VALUE,
            self.netmiko_constants.FAST_CLI: False,
            self.netmiko_constants.AUTO_CONNECT: False,
        }

    def _exec_download_commands(self, connect_handler: BaseConnection):
        hostname: str = connect_handler.find_prompt()
        config_result: str = connect_handler.send_command(self.RUNNING_CONFIG_CMD)
        neighbors_result: str = connect_handler.send_command(self.CDP_NEIGHBORS_CMD)
        device_type: str = connect_handler.send_command(self.SHOW_VERSION)

        return config_result, neighbors_result, hostname, device_type

    def _exec_upload_command(self, connect_handler: BaseConnection, running_config: list[str]):
        return connect_handler.send_config_set(running_config)

    def _exec_hostname_and_cdp_commands(self, connect_handler: BaseConnection, timer=5, holdtime=10):
        command_set = [
            self.CDP_TIMER.format(timer),
            self.CDP_HOLDTIME.format(holdtime)
        ]

        return connect_handler.send_config_set(command_set)

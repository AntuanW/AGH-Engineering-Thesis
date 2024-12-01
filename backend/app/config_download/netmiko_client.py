from netmiko import BaseConnection, ConnectHandler, redispatch
import time

import utils.connection_constants as cc
from .dto.download_request_dto import ConfigDownloadDto
from .config import DEVICE_USERNAME, DEVICE_PASSWORD


class NetmikoClient:
    MODE_DIRECT = "cisco_ios"
    CONN_MODE = "generic_termserver_telnet"
    GLOBAL_DELAY_FACTOR_VALUE = 3.0
    RUNNING_CONFIG_CMD = "show running-config"

    def download_config_from_device(self, device: ConfigDownloadDto) -> str:
        connect_handler: BaseConnection = self._get_connection_handler(
            str(device.ip), device.port, DEVICE_USERNAME, DEVICE_PASSWORD
        )

        with connect_handler:
            time.sleep(1)
            read_channel: str = connect_handler.read_channel()
            if read_channel.find("[yes/no]"):
                connect_handler.write_channel("no\r")
                time.sleep(1)
            redispatch(connect_handler, device_type=self.MODE_DIRECT)

            if not connect_handler.check_enable_mode():
                connect_handler.enable()

            running_config: str = connect_handler.send_command(self.RUNNING_CONFIG_CMD)
        return running_config

    def _get_connection_handler(self, ip: str, port: int, uname: str, pwd: str) -> BaseConnection:
        handler_dict: dict = self._build_connection_dict(ip, port, uname, pwd)
        return ConnectHandler(**handler_dict)

    def _build_connection_dict(self, ip: str, port: int, uname: str, pwd: str) -> dict:
        return {
            cc.IP: ip,
            cc.PORT: port,
            cc.USERNAME: uname,
            cc.PASSWORD: pwd,
            cc.DEVICE_TYPE: self.CONN_MODE,
            cc.GLOBAL_DELAY_FACTOR: self.GLOBAL_DELAY_FACTOR_VALUE
        }

from netmiko import BaseConnection, ConnectHandler, redispatch
import time

import app.config_download.utils.connection_constants as cc
from .dto.download_request_dto import SingleDeviceConfigDto, SingleDeviceConfigDtoV2
from .config import DEVICE_USERNAME, DEVICE_PASSWORD


class NetmikoClient:
    MODE_DIRECT = "cisco_ios"
    CONN_MODE = "generic_termserver_telnet"
    GLOBAL_DELAY_FACTOR_VALUE = 3.0
    RUNNING_CONFIG_CMD = "show running-config"
    CDP_NEIGHBORS_CMD = "show cdp neighbors"

    # TODO: change back to SingleDeviceDto when confirmed in tests
    def download_config_from_device(self, device: SingleDeviceConfigDtoV2) -> str:
        running_config: str = self._exec_and_save_command(device, self.RUNNING_CONFIG_CMD)
        return running_config

    def get_device_neighbours(self, device: SingleDeviceConfigDtoV2) -> str:
        cdp_neighbors: str = self._exec_and_save_command(device, self.CDP_NEIGHBORS_CMD)
        # TODO: cdp neighbors feedback parsing
        return cdp_neighbors


    def _exec_and_save_command(self, device: SingleDeviceConfigDtoV2, cmd: str) -> str:
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

            cmd_result: str = connect_handler.send_command(cmd)
        return cmd_result

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
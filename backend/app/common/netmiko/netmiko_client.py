from netmiko import BaseConnection, ConnectHandler, redispatch
import time

from .config import DEVICE_USERNAME, DEVICE_PASSWORD
from app.config_download.utils.download_config_request import PhysicalDevice
import netmiko_constants as nc


class NetmikoClient:
    MODE_DIRECT = "cisco_ios"
    CONN_MODE = "generic_termserver_telnet"
    GLOBAL_DELAY_FACTOR_VALUE = 3.0
    RUNNING_CONFIG_CMD = "show running-config"
    CDP_NEIGHBORS_CMD = "show cdp neighbors"

    def download_config_from_device(self, device: PhysicalDevice) -> tuple[str, str]:
        running_config, neighbors_str = self._exec_and_save_command(device,
                                                                    self.RUNNING_CONFIG_CMD,
                                                                    self.CDP_NEIGHBORS_CMD)
        return running_config, neighbors_str

    def _exec_and_save_command(self,
                               device: PhysicalDevice,
                               config_cmd: str,
                               neighbors_cmd) -> tuple[str, str]:
        connect_handler: BaseConnection = self._get_connection_handler(
            device.ip_address, device.port, DEVICE_USERNAME, DEVICE_PASSWORD
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

            config_result: str = connect_handler.send_command(config_cmd)
            neighbors_result: str = connect_handler.send_command(neighbors_cmd)

        return config_result, neighbors_result

    def _get_connection_handler(self, ip: str, port: int, uname: str, pwd: str) -> BaseConnection:
        handler_dict: dict = self._build_connection_dict(ip, port, uname, pwd)
        return ConnectHandler(**handler_dict)

    def _build_connection_dict(self, ip: str, port: int, uname: str, pwd: str) -> dict:
        return {
            nc.IP: ip,
            nc.PORT: port,
            nc.USERNAME: uname,
            nc.PASSWORD: pwd,
            nc.DEVICE_TYPE: self.CONN_MODE,
            nc.GLOBAL_DELAY_FACTOR: self.GLOBAL_DELAY_FACTOR_VALUE
        }
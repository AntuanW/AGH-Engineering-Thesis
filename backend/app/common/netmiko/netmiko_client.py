from netmiko import BaseConnection, ConnectHandler, redispatch
import time
from pydantic import BaseModel

from .config import DEVICE_USERNAME, DEVICE_PASSWORD
import netmiko_constants as nc
from app.models.mapped_device import MappedDeviceModel
from .netmiko_action import NetmikoAction
from .netmiko_device import NetmikoDevice


class NetmikoClient:
    MODE_DIRECT = "cisco_ios"
    CONN_MODE = "generic_termserver_telnet"
    GLOBAL_DELAY_FACTOR_VALUE = 3.0
    RUNNING_CONFIG_CMD = "show running-config"
    CDP_NEIGHBORS_CMD = "show cdp neighbors"

    def upload_config_to_device(self, device: MappedDeviceModel):
        self._exec_netmiko_action(device, NetmikoAction.UPLOAD_COMMAND_SET)

    def download_config_from_device(self, device: NetmikoDevice) -> tuple[str, str]:
        running_config, neighbors_str = self._exec_netmiko_action(device, NetmikoAction.DOWNLOAD_RUNNING_CONFIG)
        return running_config, neighbors_str

    def _exec_netmiko_action(self, device: NetmikoDevice | MappedDeviceModel, action: NetmikoAction):
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

            match action:
                case NetmikoAction.DOWNLOAD_RUNNING_CONFIG:
                    result = self._exec_download_commands(connect_handler)
                case NetmikoAction.UPLOAD_COMMAND_SET:
                    result = self._exec_upload_command(connect_handler, device.mapped_config)

        return result

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

    def _exec_download_commands(self, connect_handler: BaseConnection):
        config_result: str = connect_handler.send_command(self.RUNNING_CONFIG_CMD)
        neighbors_result: str = connect_handler.send_command(self.CDP_NEIGHBORS_CMD)
        return config_result, neighbors_result

    def _exec_upload_command(self, connect_handler: BaseConnection, running_config: list[str]):
        return connect_handler.send_config_set(running_config)

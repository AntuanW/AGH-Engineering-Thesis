from .netmiko_connection_config import NetmikoConnectionConfig
from ..running_config.dto.topology_response_dto import DeviceConfigInfo
from .util.netmiko_device import NetmikoDevice
from .exceptions.config_upload_exceptions import DeviceConfigError, DeviceConnectionError
from netmiko import NetmikoTimeoutException, NetmikoAuthenticationException, ConfigInvalidException


class ConfigUploadService:
    def build_netmiko_devices(self, topology_config: list[DeviceConfigInfo]):
        devices: list[NetmikoDevice] = []
        netmiko_connection_config = NetmikoConnectionConfig()
        for device_config_info in topology_config:
            netmiko_device = NetmikoDevice(
                device_type=netmiko_connection_config.get_device_type(),
                host=netmiko_connection_config.get_host(),
                username=netmiko_connection_config.get_username(),
                password=netmiko_connection_config.get_password(),
                config=netmiko_connection_config.get_config(device_config_info.dev_running_config)
            )
            devices.append(netmiko_device)
        return devices

    def upload_configs(self, devices: list[NetmikoDevice]):
        for device in devices:
            try:
                with device:
                    device.send_config_commands()
            except NetmikoTimeoutException as e:
                raise DeviceConnectionError(f"Failed to connect to {device.host}. Error: {e}")
            except NetmikoAuthenticationException as e:
                raise DeviceConnectionError(f"Failed to authenticate to {device.host}. Error: {e}")
            except ConfigInvalidException as e:
                raise DeviceConfigError(f"Invalid config for {device.host}. Error: {e}")
            except Exception as e:
                raise DeviceConfigError(f"Failed to send config to {device.host}. Error: {e}")

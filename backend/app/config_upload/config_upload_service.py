from .netmiko_config_builder import NetmikoConfigBuilder
from ..running_config.util.device_config_types import DeviceConfigInfo
from .util.netmiko_device import NetmikoDevice
from .exceptions.config_upload_exceptions import DeviceConfigError, DeviceConnectionError


class ConfigUploadService:
    def build_netmiko_devices(self, topology_config: list[DeviceConfigInfo]):
        devices: list[NetmikoDevice] = []
        netmiko_config_builder = NetmikoConfigBuilder()
        for device_config_info in topology_config:
            netmiko_device = NetmikoDevice(
                device_type=netmiko_config_builder.get_device_type(),
                host=netmiko_config_builder.get_host(),
                username=netmiko_config_builder.get_username(),
                password=netmiko_config_builder.get_password(),
                config=netmiko_config_builder.get_config(device_config_info['dev_running_config'])
            )
            devices.append(netmiko_device)
        return devices

    def upload_configs(self, devices: list[NetmikoDevice]):
        for device in devices:
            try:
                with device:
                    try:
                        device.send_config_commands()
                    except Exception as e:
                        raise DeviceConfigError(f"Failed to send config to {device.host}. Error:{e}")
            except Exception as e:
                raise DeviceConnectionError(f"Failed to connect to {device.host}. Error:{e}")

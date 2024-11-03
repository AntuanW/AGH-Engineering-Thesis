from .netmiko_config_builder import NetmikoConfigBuilder
from ..running_config.util.device_config_types import DeviceConfigInfo
from .models.netmiko_device import NetmikoDevice


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
            device.connect()
            device.send_config_commands()
            device.disconnect()

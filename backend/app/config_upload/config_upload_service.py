from ..models.mapped_device import MappedDeviceModel
from .util.netmiko_device import NetmikoDevice
from .exceptions.config_upload_exceptions import DeviceConfigError, DeviceConnectionError
from netmiko import NetmikoTimeoutException, NetmikoAuthenticationException, ConfigInvalidException


class ConfigUploadService:
    def build_netmiko_devices(self, devices: list[MappedDeviceModel]):
        netmiko_devices: list[NetmikoDevice] = []
        for device in devices:
            netmiko_device = NetmikoDevice(
                device_type=device.netmiko_device_type.value,
                ip=str(device.ip_address),
                port=device.port,
                config=device.mapped_config
            )
            netmiko_devices.append(netmiko_device)
        return netmiko_devices

    def upload_configs(self, devices: list[NetmikoDevice]):
        for device in devices:
            try:
                with device:
                    device.send_config_commands()
            except NetmikoTimeoutException as e:
                raise DeviceConnectionError(f"Failed to connect to {device.ip}:{device.port}. Error: {e}")
            except NetmikoAuthenticationException as e:
                raise DeviceConnectionError(f"Failed to authenticate to {device.ip}:{device.port}. Error: {e}")
            except ConfigInvalidException as e:
                raise DeviceConfigError(f"Invalid config for {device.ip}:{device.port}. Error: {e}")
            except Exception as e:
                raise DeviceConfigError(f"Failed to send config to {device.ip}:{device.port}. Error: {e}")

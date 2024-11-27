import unittest

from app.config_upload.config_upload_service import ConfigUploadService
from app.config_upload.util.netmiko_types import NetmikoDeviceType
from app.models.connection import ConnectionModel
from app.models.mapped_device import MappedDeviceModel
from pydantic.networks import IPvAnyAddress


class TestConfigUploadService(unittest.TestCase):
    def test_build_netmiko_devices(self):
        mapped_devices = [
            MappedDeviceModel(
                name='R11',
                netmiko_device_type=NetmikoDeviceType('cisco_ios'),
                ip_address=IPvAnyAddress('172.17.145.10'),
                port=2001,
                neighbours=[
                    ConnectionModel(
                        neighbour_name='R12',
                        from_interface='GigabitEthernet0/0',
                        to_interface='GigabitEthernet0/0',
                    )
                ],
                mapped_config=['show version', 'show running-config'],
            ),
            MappedDeviceModel(
                name='R12',
                netmiko_device_type=NetmikoDeviceType('cisco_ios'),
                ip_address=IPvAnyAddress('172.17.145.10'),
                port=2002,
                neighbours=[
                    ConnectionModel(
                        neighbour_name='R11',
                        from_interface='GigabitEthernet0/0',
                        to_interface='GigabitEthernet0/0',
                    )
                ],
                mapped_config=['show version', 'show running-config'],
            ),
        ]

        service = ConfigUploadService()
        netmiko_devices = service.build_netmiko_devices(mapped_devices)
        assert netmiko_devices is not None
        assert len(netmiko_devices) == 2
        assert netmiko_devices[0].device_type == 'cisco_ios'
        assert netmiko_devices[0].ip == '172.17.145.10'
        assert netmiko_devices[0].port == 2001
        assert netmiko_devices[0].config == ['show version', 'show running-config']

from unittest.mock import MagicMock

from app.config_upload.util.netmiko_types import NetmikoDeviceType
from app.repository.mapping_repository import MappingRepository
from app.models.mapped_device import MappedDeviceModel
from app.models.connection import ConnectionModel

from pydantic.networks import IPvAnyAddress


def test_basic_connection():
    repo = MappingRepository()
    repo.get_collection()


def test_find_devices_by_group():
    mock_lab_group = 1
    mock_mapping = {
        'lab_group': mock_lab_group,
        'mapped_devices': [
            {
                'name': 'R11',
                'netmiko_device_type': 'cisco_ios',
                'ip_address': '172.17.145.10',
                'port': 2001,
                'neighbours': [
                    {
                        'neighbour_name': 'R12',
                        'from_interface': 'GigabitEthernet0/0',
                        'to_interface': 'GigabitEthernet0/0',
                    }
                ],
                'mapped_config': ['show version', 'show running-config'],
            },
            {
                'name': 'R12',
                'netmiko_device_type': 'cisco_ios',
                'ip_address': '172.17.145.10',
                'port': 2002,
                'neighbours': [
                    {
                        'neighbour_name': 'R11',
                        'from_interface': 'GigabitEthernet0/0',
                        'to_interface': 'GigabitEthernet0/0',
                    }
                ],
                'mapped_config': ['show version', 'show running-config'],
            },
        ],
    }

    expected_devices = [
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

    repo = MappingRepository()
    repo.find_one = MagicMock(return_value=mock_mapping)

    found_devices = repo.find_devices_by_group(mock_lab_group)

    assert found_devices is not None
    assert found_devices == expected_devices
    assert isinstance(found_devices, list)
    assert isinstance(found_devices[0], MappedDeviceModel)

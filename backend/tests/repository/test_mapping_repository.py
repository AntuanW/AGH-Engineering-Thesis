from unittest.mock import MagicMock
from bson.objectid import ObjectId

from app.models.mapping import MappingModel
from app.repository.mapping_repository import MappingRepository
from app.models.mapped_device import MappedDeviceModel
from app.running_config.util.device_config_types import DeviceType
from app.common.netmiko.netmiko_device_type import NetmikoDeviceType


def test_basic_connection():
    repo = MappingRepository()
    repo.get_collection()


def test_find_devices_by_group():
    mock_lab_group_number = 1
    mock_mapping_id = ObjectId('5f8f8f8f8f8f8f8f8f8f8f8f')
    mock_topology_id = '5f8f8f8f8f8f8f8f8f8f8f8f'
    mock_mapped_device = MappedDeviceModel(
        name='Router',
        ip_address='0.0.0.0',
        port=2001,
        device_type=DeviceType.ROUTER,
        netmiko_device_type=NetmikoDeviceType.CISCO_IOS,
        mapped_config=[],
        neighbours=[]
    )
    mock_mapping = {
        '_id': mock_mapping_id,
        'lab_group_number': mock_lab_group_number,
        'topology_id': mock_topology_id,
        'mapped_devices': [mock_mapped_device]
    }

    expected_mapping = MappingModel(**mock_mapping)

    repo = MappingRepository()
    repo.find_devices_by_group = MagicMock(return_value=mock_mapping['mapped_devices'])
    found_mapping = repo.find_devices_by_group(mock_lab_group_number, mock_topology_id)

    assert found_mapping is not None
    assert found_mapping == expected_mapping.mapped_devices

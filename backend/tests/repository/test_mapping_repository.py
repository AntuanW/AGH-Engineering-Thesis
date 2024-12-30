from unittest.mock import MagicMock
from bson.objectid import ObjectId

from app.models.mapping import MappingCollectionModel, MappingType
from app.repository.mapping_repository import MappingRepository
from app.models.mapped_device import MappedDeviceModel
from app.running_config.util.device_config_types import DeviceType
from app.common.netmiko.netmiko_device_type import NetmikoDeviceType


def test_basic_connection():
    repo = MappingRepository()
    repo.get_collection()


def test_find_devices_by_group():
    mock_lab_group_number = 1
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
        'name': 'test',
        'type': MappingType.CREATED_FROM_PKT,
        'topology_id': mock_topology_id,
        'mappings': {1: [mock_mapped_device]}
    }

    expected_mapping = MappingCollectionModel(**mock_mapping)

    repo = MappingRepository()
    repo.find_devices_by_group = MagicMock(return_value=mock_mapping['mappings'])
    found_mappings = repo.find_devices_by_group(mock_lab_group_number, mock_topology_id)

    print(found_mappings)

    assert found_mappings is not None
    assert found_mappings == expected_mapping.mappings

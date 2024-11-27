from bson import ObjectId
from unittest.mock import MagicMock

from app.repository.device_repository import DeviceRepository
from app.models.device import DeviceModel

def test_basic_connection():
    repo = DeviceRepository()
    repo.get_collection()


def test_find_by_id():
    mock_device_id = ObjectId('5f8f8f8f8f8f8f8f8f8f8f8f')
    mock_device_data = {
        '_id': mock_device_id,
        'name': 'test_name',
        'type': 'test_type'
    }
    expected_device = DeviceModel(**mock_device_data)

    repo = DeviceRepository()
    repo.find_one = MagicMock(return_value=mock_device_data)

    found_device = repo.find_by_id(mock_device_id)

    assert found_device is not None
    assert found_device == expected_device
    assert isinstance(found_device, DeviceModel)

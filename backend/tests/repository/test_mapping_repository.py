from unittest.mock import MagicMock

from app.config_upload.util.netmiko_types import NetmikoDeviceType
from app.repository.mapping_repository import MappingRepository
from app.models.mapped_device import MappedDeviceModel
from app.models.connection import ConnectionModel
from app.models.mapping import MappingModel


def test_basic_connection():
    repo = MappingRepository()
    repo.get_collection()


def test_find_devices_by_group():
    repo = MappingRepository()
    found_devices = repo.find_devices_by_group(1)

    assert found_devices is not []
    assert len(found_devices) == 3
    assert isinstance(found_devices, list)
    assert isinstance(found_devices[0], MappedDeviceModel)

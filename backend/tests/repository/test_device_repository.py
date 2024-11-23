from bson import ObjectId

from app.repository.device_repository import DeviceRepository
from app.models.device import DeviceModel

def test_basic_connection():
    repo = DeviceRepository()
    repo.get_collection()


def test_find_by_id():
    repo = DeviceRepository()
    device = repo.find_by_id(ObjectId('671b941494283ece5865951b'))
    assert device is not None
    assert type(device) is DeviceModel

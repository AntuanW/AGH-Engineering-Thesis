from app.repository.in_use_device_repository import InUseDeviceRepository


def test_basic_connection():
    repo = InUseDeviceRepository()
    repo.get_collection()

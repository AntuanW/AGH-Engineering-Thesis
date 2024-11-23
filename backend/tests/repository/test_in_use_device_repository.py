from app.repository.in_use_device_repository import InUseDeviceRepository


def test_basic_connection():
    repo = InUseDeviceRepository()
    repo.get_collection()


def test_find_all():
    repo = InUseDeviceRepository()
    in_use_devices = repo.find_all()
    assert in_use_devices is None

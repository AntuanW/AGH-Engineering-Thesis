from app.repository.device_repository import DeviceRepository

def test_basic_connection():
    repo = DeviceRepository()
    repo.get_collection()

from app.repository.in_use_device_repository import InUseDeviceRepository
from app.models.in_use_device import InUseDeviceModel
from models.pydantic_object_id import PydanticObjectId

class TestConnectionRepository:
    def test_basic_connection(self):
        repo = InUseDeviceRepository()
        repo.get_collection()

    def test_find_all(self):
        repo = InUseDeviceRepository()
        device = InUseDeviceModel(
            device_id=PydanticObjectId("TODO: Fix me!"),
            name="dev1_name",
            lab_group_id=0
        )
        device_id = repo.insert(device)

        devices = repo.find_all()

        try:
            assert len(devices) > 0
            assert type(device[0]) is InUseDeviceModel
        finally:
            assert repo.delete_one({"_id": device_id}) == 1
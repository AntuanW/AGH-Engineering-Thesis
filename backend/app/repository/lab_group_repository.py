from .base_repository import BaseRepository
from pymongo.collection import Collection
from app.models.lab_group import LabGroupModel


class LabGroupRepository(BaseRepository[LabGroupModel]):
    def get_collection(self) -> Collection:
        return self.db.get_collection('lab_groups')

    def insert(self, lab_group: LabGroupModel):
        return super().insert(lab_group.model_dump())

    def list_names(self):
        return [{"name": str(obj["lab_group_number"]), "_id": str(obj["_id"])}
                for obj in self.get_collection().find({}, {"lab_group_number": 1})]

    def get_all_group_ids(self) -> list[int]:
        return [group.lab_group_number for group in self.find_objects({})]
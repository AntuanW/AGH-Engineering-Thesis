from .base_repository import BaseRepository
from pymongo.collection import Collection
from app.models.lab_group import LabGroupModel


class LabGroupRepository(BaseRepository[LabGroupModel]):
    def get_collection(self) -> Collection:
        return self.db.get_collection('lab_groups')

    def insert(self, lab_group: LabGroupModel):
        return super().insert(lab_group.model_dump())

    def get_all_group_ids(self) -> list[int]:
        return [group.lab_group_number for group in self.find_objects({})]
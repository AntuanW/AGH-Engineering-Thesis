from pydantic import BaseModel
from .rack import RackModel


class LabGroupModel(BaseModel):
    lab_group_number: int
    rack: RackModel

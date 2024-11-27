from pydantic import BaseModel
from .rack import RackModel


class LabGroupModel(BaseModel):
    group_number: int
    rack: RackModel

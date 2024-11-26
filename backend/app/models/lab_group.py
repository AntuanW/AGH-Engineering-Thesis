from pydantic import BaseModel
from .rack import RackModel


class LabGroupModel(BaseModel):
    group: int
    rack: RackModel

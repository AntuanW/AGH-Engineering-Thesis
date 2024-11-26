from pydantic import BaseModel
from .pydantic_object_id import PydanticObjectId


class LabGroupModel(BaseModel):
    group: int
    rack_id: PydanticObjectId

from pydantic import BaseModel
from .pydantic_object_id import PydanticObjectId


class InUseDeviceModel(BaseModel):
    device_id: PydanticObjectId
    name: str
    lab_group_id: int

from pydantic import BaseModel
from .pydantic_object_id import PydanticObjectId


class InUseDeviceModel(BaseModel):
    device_id: PydanticObjectId
    name: str
    group: str

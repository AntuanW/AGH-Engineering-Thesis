from pydantic import BaseModel
from bson import ObjectId

class InUseDeviceModel(BaseModel):
    device_id: ObjectId
    name: str
    group: str

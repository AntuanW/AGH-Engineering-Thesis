from pydantic import BaseModel


class InUseDeviceModel(BaseModel):
    id: str
    physical_device_id: str
    group: int

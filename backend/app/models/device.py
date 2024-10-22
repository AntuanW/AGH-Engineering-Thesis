from pydantic import BaseModel

class DeviceModel(BaseModel):
    name: str
    type: str
    # TODO device model

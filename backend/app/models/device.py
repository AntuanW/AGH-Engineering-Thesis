from pydantic import BaseModel
from app.running_config.utils.device_config_constants import DeviceType


class DeviceModel(BaseModel):
    name: str
    device_type: DeviceType
    interfaces: list[str]
    commands: list[str]
    rack_id: int

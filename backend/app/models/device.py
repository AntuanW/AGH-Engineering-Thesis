from pydantic import BaseModel
from app.running_config.util.device_config_types import DeviceType


class DeviceModel(BaseModel):
    name: str
    device_type: DeviceType
    interfaces: list[str]
    commands: list[str]
    rack_id: int

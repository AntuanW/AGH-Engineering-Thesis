from pydantic import BaseModel
from app.running_config.dto.topology_response_dto import DeviceType


class DeviceModel(BaseModel):
    name: str
    device_type: DeviceType
    interfaces: list[str]
    commands: list[str]
    rack_id: int

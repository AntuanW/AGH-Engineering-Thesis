from pydantic import BaseModel
from app.running_config.util.device_config_types import DeviceConfigInfo


class TopologyModel(BaseModel):
    name: str
    topology: list[DeviceConfigInfo]

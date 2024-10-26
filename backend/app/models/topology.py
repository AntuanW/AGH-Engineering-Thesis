from pydantic import BaseModel
from app.running_config.util.device_config_types import DeviceConfigInfo


class TopologyModel(BaseModel):
    topology: list[DeviceConfigInfo]

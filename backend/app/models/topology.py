from pydantic import BaseModel
from app.running_config.dto.topology_response_dto import DeviceConfigInfo


class TopologyModel(BaseModel):
    name: str
    topology: list[DeviceConfigInfo]

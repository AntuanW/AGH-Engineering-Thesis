from pydantic import BaseModel
from app.running_config.util.device_config_types import DeviceType
from app.models.connection import ConnectionModel

class DownloadedConfig(BaseModel):
    name: str
    device_type: DeviceType
    neighbours: list[ConnectionModel]


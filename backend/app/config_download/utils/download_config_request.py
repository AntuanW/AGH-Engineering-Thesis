from pydantic import BaseModel
from app.common.netmiko.netmiko_device import NetmikoDevice


class DownloadConfigRequest(BaseModel):
    lab_name: str
    lab_group: int
    devices: list[NetmikoDevice]

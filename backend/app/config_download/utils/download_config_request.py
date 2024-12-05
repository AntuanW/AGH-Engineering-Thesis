from pydantic import BaseModel
from pydantic.networks import IPvAnyNetwork


class PhysicalDevice(BaseModel):
    name: str
    ip_address: str
    port: int


class DownloadConfigRequest(BaseModel):
    lab_name: str
    lab_group: str
    devices: list[PhysicalDevice]

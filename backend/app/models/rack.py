from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress

from app.models.device import DeviceModel


class RackModel(BaseModel):
    config_port_ip_address: IPvAnyAddress
    config_ports: list[int]
    devices: list[DeviceModel]

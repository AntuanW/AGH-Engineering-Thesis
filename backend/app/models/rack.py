from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress


class RackModel(BaseModel):
    rack_id: int
    config_port_ip_address: IPvAnyAddress
    config_ports: list[int]

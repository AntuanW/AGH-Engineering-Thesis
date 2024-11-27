from pydantic import BaseModel


class RackModel(BaseModel):
    rack_id: int
    config_port_ip_address: str
    config_ports: list[int]

from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress


class RackModel(BaseModel):
    ip_address: IPvAnyAddress
    port_range: list[int]

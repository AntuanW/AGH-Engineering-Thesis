from pydantic import BaseModel
from pydantic.networks import IPvAnyNetwork


class Connection(BaseModel):
    connection_name: str
    connection_iface: str
    original_iface: str


class ConfigDownloadDto(BaseModel):
    name: str
    ip: IPvAnyNetwork
    port: int
    connections: list[Connection]

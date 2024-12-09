from pydantic import BaseModel


class NetmikoDevice(BaseModel):
    name: str
    ip_address: str
    port: int

from pydantic import BaseModel


class NetmikoDevice(BaseModel):
    ip_address: str
    port: int

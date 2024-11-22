from pydantic import BaseModel


class ConnectionModel(BaseModel):
    device1: str
    interface1: str
    device2: str
    interface2: str



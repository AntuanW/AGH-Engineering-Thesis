from pydantic import BaseModel


class ConnectionModel(BaseModel):
    neighbour_name: str
    from_interface: str
    to_interface: str

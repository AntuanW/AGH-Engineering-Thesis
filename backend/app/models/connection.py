from pydantic import BaseModel


class ConnectionModel(BaseModel):
    origin_name: str
    neighbour_name: str
    from_interface: str
    to_interface: str

    # A connection from A to B and from B to A are equal.
    # If you need to compare references
    def __hash__(self):
        return hash(self.origin_name + self.from_interface) + hash(self.neighbour_name + self.to_interface)

    def __eq__(self, other: "ConnectionModel"):
        return self.__hash__() == other.__hash__()

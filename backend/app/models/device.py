import re

from pydantic import BaseModel
from app.running_config.util.device_config_types import DeviceType
from enum import Enum


class InterfaceType(Enum):
    GI = "Gi"
    FA = "Fa"
    SERIAL = "Serial"
    TEL = "Te"
    VLAN = "Vlan"
    ATM = "ATM"
    UCSEL = "ucsel"
    ESE = "Embedded-Service-Engine"

    @staticmethod
    def from_name(name: str) -> "InterfaceType":
        for if_type in InterfaceType:
            if if_type.value in name:
                return if_type


class Interface(BaseModel):
    type: InterfaceType
    value: str

    def __init__(self, name: str = None, /, **data):
        if name is None:
            super().__init__(**data)
            return

        try:
            if_name = re.findall("^[^0-9]*", name)[0]
            value = re.findall("(?:[0-9]+/)*[0-9]+", name)[0]
            type_ = InterfaceType.from_name(if_name)
            print(value, type_)
            super().__init__(value=value, type=type_)
        except IndexError:
            raise ValueError(f"Invalid interface name: {name}")


    def __repr__(self):
        return f"Interface({self.type.value}{self.value})"

    def port_number(self) -> int:
        """Returns the last number in interface value, ex Gi0/1/16 -> 16"""
        return int(self.value.split("/")[-1])

    def prefix(self) -> str:
        """Returns interface value without port number, ex. 'Gi0/1/5' -> '0/1/' """
        return re.findall("(?:[0-9]/)+|$", self.value)[0]



class DeviceModel(BaseModel):
    name: str
    device_type: DeviceType
    interfaces: list[Interface]
    commands: list[str]
    rack_id: int

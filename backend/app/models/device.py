import re

from pydantic import BaseModel
from app.running_config.util.device_config_types import DeviceType
from enum import Enum


class InterfaceType(str, Enum):
    GI = "GigabitEthernet"
    FA = "FastEthernet"
    TE = "TenGigabitEthernet"
    SERIAL = "Serial"
    VLAN = "Vlan"
    ATM = "ATM"
    UCSEL = "ucsel"
    ESE = "Embedded-Service-Engine"
    PC = "PC"

    @staticmethod
    def from_name(name: str) -> str:
        for if_type in InterfaceType:
            if if_type[:2] in name:
                return if_type

    def compatible_types(self):
        match self.value:
            case InterfaceType.GI:
                return InterfaceType.FA, InterfaceType.TE
            case InterfaceType.FA:
                return InterfaceType.GI, InterfaceType.TE
            case InterfaceType.TE:
                return InterfaceType.FA, InterfaceType.GI
            case _:
                return ()


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
            super().__init__(value=value, type=type_)
        except IndexError:
            raise ValueError(f"Invalid interface name: {name}")


    def __repr__(self):
        return f"Interface({self.type.value}{self.value})"

    def __str__(self):
        return self.type.value + self.value

    def __hash__(self):
        return self.__str__().__hash__()

    def __eq__(self, other):
        return self.type == other.type and self.value == other.value

    def port_number(self) -> int:
        """Returns the last number in interface value, ex. Gi0/1/16 -> 16"""
        return int(self.value.split("/")[-1])

    def prefix(self) -> str:
        """Returns interface value without port number, ex. 'Gi0/1/5' -> '0/1/' """
        return re.findall("(?:[0-9]/)+|$", self.value)[0]

    def short_name(self) -> str:
        """Returns interface short name, ex. GigabitEthernet0/1/1 -> Gi0/1/1"""
        type_mapping = {
            InterfaceType.GI: "Gi",
            InterfaceType.FA: "Fa",
            InterfaceType.TE: "Te",
            InterfaceType.SERIAL: "Se",
            InterfaceType.VLAN: "Vlan",
            InterfaceType.ATM: "ATM",
            InterfaceType.UCSEL: "ucsel",
            InterfaceType.ESE: "ESE",
            InterfaceType.PC: "PC"
        }
        return type_mapping[self.type] + self.value

class DeviceModel(BaseModel):
    name: str
    device_type: DeviceType
    interfaces: list[Interface]
    commands: list[str]
    rack_id: int

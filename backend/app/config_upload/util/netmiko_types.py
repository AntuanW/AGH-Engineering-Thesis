from enum import Enum


class NetmikoDeviceType(str, Enum):
    CISCO_IOS = 'cisco_ios'
    UNKNOWN = 'UNKNOWN'

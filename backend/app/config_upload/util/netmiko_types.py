from enum import Enum


class NetmikoDeviceType(str, Enum):
    CISCO_IOS = 'generic_termserver_telnet'
    UNKNOWN = 'UNKNOWN'

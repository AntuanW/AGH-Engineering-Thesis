from enum import Enum


class XmlConfigConstants:
    PACKET_TRACER_TAG: str = "PACKETTRACER5"
    NETWORK_TAG: str = "NETWORK"
    DEVICES_TAG: str = "DEVICES"
    DEVICE_TAG: str = "DEVICE"
    ENGINE_TAG: str = "ENGINE"
    RUNNING_CONFIG_TAG: str = "RUNNINGCONFIG"
    LINE_TAG: str = "LINE"
    DEVICE_TYPE_TAG: str = "DEVICE_TYPE"


class DeviceType(Enum):
    ROUTER = 1
    SWITCH = 2
    UNKNOWN = 3


class DeviceConfigInfo:
    def __init__(self, dev_type: DeviceType, running_config: list[str]):
        self.dev_type: DeviceType = dev_type
        self.running_config: list[str] = running_config
from enum import Enum
from pydantic import BaseModel


class XmlConfigConstants:
    PACKET_TRACER_TAG: str = "PACKETTRACER5"
    NETWORK_TAG: str = "NETWORK"
    DEVICES_TAG: str = "DEVICES"
    DEVICE_TAG: str = "DEVICE"
    ENGINE_TAG: str = "ENGINE"
    RUNNING_CONFIG_TAG: str = "RUNNINGCONFIG"
    LINE_TAG: str = "LINE"
    DEVICE_TYPE_TAG: str = "DEVICE_TYPE"
    NAME_TAG: str = "NAME"
    TEXT_TAG: str = "#text"
    LINKS_TAG: str = "LINKS"
    LINK_TAG: str = "LINK"
    CABLE_TAG: str = "CABLE"
    FROM_TAG: str = "FROM"
    TO_TAG: str = "TO"
    PORT_TAG: str = "PORT"
    SAVE_REF_ID_TAG: str = "SAVE_REF_ID"


class DeviceType(Enum):
    ROUTER = 1
    SWITCH = 2
    UNKNOWN = 3


class DeviceLink(BaseModel):
    from_id: str
    from_if: str
    to_id: str
    to_if: str

    def __str__(self):
        return f"{self.from_id}:{self.from_if} <===> {self.to_id}:{self.to_if}"


class DeviceConfigInfo(BaseModel):
    dev_id: str
    dev_type: DeviceType
    def_running_config: list[str]
    dev_name: str
    dev_neighbours: list[DeviceLink]

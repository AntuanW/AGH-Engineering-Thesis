import xmltodict
import json
import re
import logging
from pathlib import Path
from .util.DeviceConfigTypes import DeviceConfigInfo, DeviceType, XmlConfigConstants
from .exceptions.ConfigExtractionExceptions import (
    XmlOpenException,
    InvalidDecryptedCmlFormatException,
    DeviceJsonParseException
)


class BasicConfigExtractor:
    tags: XmlConfigConstants = XmlConfigConstants()

    def get_topology_config_from_xml(self, decrypted_xml_path: str | Path) -> list[DeviceConfigInfo]:
        packet_tracer_dict: dict = self._create_dict_from_xml(decrypted_xml_path)
        return self._get_devices_configs_info(packet_tracer_dict)

    def _create_dict_from_xml(self, decrypted_xml_path: str | Path) -> dict:
        try:
            with open(decrypted_xml_path, 'r', encoding='utf-8') as file:
                xml = file.read()
        except OSError as exc:
            raise XmlOpenException(f"Failed to open/read {decrypted_xml_path} - {exc}")

        return xmltodict.parse(xml)

    def _get_devices_configs_info(self, topology_dict: dict) -> list[DeviceConfigInfo]:
        devices_info = []
        devices = (topology_dict[self.tags.PACKET_TRACER_TAG]
                                [self.tags.NETWORK_TAG]
                                [self.tags.DEVICES_TAG]
                                [self.tags.DEVICE_TAG])

        for device in devices:
            dev_type: DeviceType = self._extract_device_type(device)
            if dev_type != DeviceType.UNKNOWN:
                dev_config: list[str] = self._extract_running_config_details(device)
                devices_info.append(DeviceConfigInfo(dev_type, dev_config))

        return devices_info

    def _extract_running_config_details(self, device_dict: dict) -> list[str]:
        try:
            dev_running_config: list[str] = (device_dict[self.tags.ENGINE_TAG]
                                                        [self.tags.RUNNING_CONFIG_TAG])
        except KeyError:
            raise InvalidDecryptedCmlFormatException("Config extraction error - invalid format of decrypted xml.")
        return dev_running_config

    def _extract_device_type(self, device_dict: dict) -> DeviceType:
        try:
            dev_str: str = json.dumps(device_dict)
        except (ValueError, TypeError) as exc:
            raise DeviceJsonParseException(f"Failed to parse dict to json - {exc}")

        regex: str = r'"' + self.tags.DEVICE_TYPE_TAG + r'": "((\\"|[^"])*)"'
        matches: list = re.findall(regex, dev_str)

        if len(matches) == 0:
            logging.debug("Undefined device type.")
            return DeviceType.UNKNOWN

        dev_type, _ = matches[0]
        return DeviceType[dev_type.upper()]

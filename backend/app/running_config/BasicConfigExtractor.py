import xmltodict
import json
import re
import logging
from pathlib import Path
from .util.DeviceConfigTypes import DeviceConfigInfo, DeviceType, XmlConfigConstants, DeviceLink
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

        links: list[DeviceLink] = self._get_all_links(topology_dict)

        for device in devices:
            dev_type: DeviceType = self._extract_device_type(device)
            if dev_type != DeviceType.UNKNOWN:
                dev_id: str = self._get_device_id(device)
                devices_info.append(DeviceConfigInfo(
                    dev_id=dev_id,
                    dev_type=dev_type,
                    dev_running_config=self._extract_running_config_details(device),
                    dev_name=self._extract_device_name(device),
                    dev_neighbours=self._get_device_neighbours(dev_id, links)
                ))

        return devices_info

    def _extract_running_config_details(self, device_dict: dict) -> list[str]:
        try:
            dev_running_config: list[str] = (device_dict[self.tags.ENGINE_TAG]
                                                        [self.tags.RUNNING_CONFIG_TAG]
                                                        [self.tags.LINE_TAG])
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

    def _extract_device_name(self, device_dict: dict) -> str:
        try:
            dev_name: str = (device_dict[self.tags.ENGINE_TAG]
                                        [self.tags.NAME_TAG]
                                        [self.tags.TEXT_TAG])
        except KeyError:
            raise InvalidDecryptedCmlFormatException("Config extraction error - invalid format of decrypted xml.")
        return dev_name

    def _get_device_id(self, device_dict: dict) -> str:
        try:
            dev_id: str = device_dict[self.tags.ENGINE_TAG][self.tags.SAVE_REF_ID_TAG]
        except KeyError:
            raise InvalidDecryptedCmlFormatException("Failed to extract device id from decrypted xml.")
        return dev_id

    def _get_device_neighbours(self, dev_id: str, links: list[DeviceLink]) -> list[DeviceLink]:
        neighbours: list[DeviceLink] = []
        for link in links:
            if link.from_id == dev_id:
                neighbours.append(link)
        return neighbours

    def _get_all_links(self, topology_dict: dict) -> list[DeviceLink]:
        links_dict: dict = (topology_dict[self.tags.PACKET_TRACER_TAG]
                                         [self.tags.NETWORK_TAG]
                                         [self.tags.LINKS_TAG]
                                         [self.tags.LINK_TAG])
        links: list[DeviceLink] = []
        for link in links_dict:
            cable: dict = link[self.tags.CABLE_TAG]
            from_id: str = cable[self.tags.FROM_TAG]
            from_if: str = cable[self.tags.PORT_TAG][0]
            to_id: str = cable[self.tags.TO_TAG]
            to_if: str = cable[self.tags.PORT_TAG][1]
            links.append(DeviceLink(
                from_id=from_id,
                from_if=from_if,
                to_id=to_id,
                to_if=to_if
            ))
            links.append(DeviceLink(
                from_id=to_id,
                from_if=to_if,
                to_id=from_id,
                to_if=from_if
            ))
        return links

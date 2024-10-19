import xmltodict
import json
import re
from pathlib import Path
from .util.DeviceConfigTypes import DeviceConfigInfo, DeviceType, XmlConfigConstants


'''
Extract running configs from devices in xml
'''
class BasicConfigExtractor:
    tags: XmlConfigConstants = XmlConfigConstants()

    def get_topology_config_from_xml(self, decrypted_xml_path: str | Path):
        packet_tracer_dict: dict = self.create_dict_from_xml(decrypted_xml_path)
        return self.get_devices_configs_info(packet_tracer_dict)

    def create_dict_from_xml(self, decrypted_xml_path: str | Path) -> dict:
        with open(decrypted_xml_path, 'r', encoding='utf-8') as file:
            xml = file.read()
        return xmltodict.parse(xml)

    def get_devices_configs_info(self, topology_dict: dict) -> list[DeviceConfigInfo]:
        devices_info = []
        devices = (topology_dict[self.tags.PACKET_TRACER_TAG]
                                [self.tags.NETWORK_TAG]
                                [self.tags.DEVICES_TAG]
                                [self.tags.DEVICE_TAG])

        for device in devices:
            dev_type: DeviceType = self.extract_device_type(device)
            if dev_type != DeviceType.UNKNOWN:
                dev_config: list[str] = self.extract_running_config_details(device)
                devices_info.append(DeviceConfigInfo(dev_type, dev_config))

        return devices_info

    def extract_running_config_details(self, device_dict: dict) -> list[str]:
        raise NotImplementedError()

    def extract_device_type(self, device_dict: dict) -> DeviceType:
        dev_str: str = json.dumps(device_dict)
        regex: str = r'"' + self.tags.DEVICE_TYPE_TAG + r'": "((\\"|[^"])*)"'
        matches: list = re.findall(regex, dev_str)

        if len(matches) == 0:
            return DeviceType.UNKNOWN

        dev_type, _ = matches[0]
        return DeviceType[dev_type.upper()]

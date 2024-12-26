#TODO - config extraction tests
import unittest
from pathlib import Path

from bson import ObjectId

from app.repository.decrypted_xml_repository import DecryptedXMLRepository
from app.running_config.config_extractor import ConfigExtractor
from app.running_config.util.device_config_types import DeviceConfigInfo, DeviceType
from app.running_config.exceptions.config_extraction_exceptions import XmlOpenException

RESOURCES_PATH = Path(__file__).parent


class TestBasicConfigExtractor(unittest.TestCase):
    def test_get_topology_config_from_xml(self):
        decrypted_xml_repository: DecryptedXMLRepository = DecryptedXMLRepository()
        topology = decrypted_xml_repository.find_object({"_id": ObjectId("671e2fd1af242f362075d943")})
        basic_config_extractor: ConfigExtractor = ConfigExtractor()

        device_counter: dict = {DeviceType.ROUTER: 0, DeviceType.SWITCH: 0, DeviceType.PC: 0}

        result: list[DeviceConfigInfo] = basic_config_extractor.get_topology_config_from_xml(topology)
        for dev in result:
            device_counter[dev.dev_type] += 1

        assert len(result) == 9, f"Failed to parse xml - invalid number of devices found: 9 != {len(result)}"
        assert device_counter[DeviceType.ROUTER] == 3, "Routers counter is not equal to 3"
        assert device_counter[DeviceType.SWITCH] == 6, "Switches counter is not equal to 6"
        assert device_counter[DeviceType.PC] == 0, "Switches counter is not equal to 0"

    def test_get_topology_config_from_xml_pc(self):
        decrypted_xml_repository: DecryptedXMLRepository = DecryptedXMLRepository()
        topology = decrypted_xml_repository.find_object({"_id": ObjectId("674dab18bbbd7e2648903669")})
        basic_config_extractor: ConfigExtractor = ConfigExtractor()

        device_counter: dict = {DeviceType.ROUTER: 0, DeviceType.SWITCH: 0, DeviceType.PC: 0}

        result: list[DeviceConfigInfo] = basic_config_extractor.get_topology_config_from_xml(topology)
        for dev in result:
            device_counter[dev.dev_type] += 1

        assert len(result) == 6, f"Failed to parse xml - invalid number of devices found: 6 != {len(result)}"
        assert device_counter[DeviceType.ROUTER] == 1, "Routers counter is not equal to 1"
        assert device_counter[DeviceType.SWITCH] == 3, "Switches counter is not equal to 3"
        assert device_counter[DeviceType.PC] == 2, "Switches counter is not equal to 2"

    def test_get_topology_config_from_xml_raises_exception(self):
        xml_file_path: Path = RESOURCES_PATH.joinpath('resources/non-existent-topology.xml')
        basic_config_extractor: ConfigExtractor = ConfigExtractor()
        self.assertRaises(XmlOpenException, basic_config_extractor.get_topology_config_from_xml, xml_file_path)

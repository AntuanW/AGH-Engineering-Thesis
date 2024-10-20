import unittest
from pathlib import Path
from app.running_config.BasicConfigExtractor import BasicConfigExtractor
from app.running_config.util.DeviceConfigTypes import DeviceConfigInfo, DeviceType
from app.running_config.exceptions.ConfigExtractionExceptions import XmlOpenException

RESOURCES_PATH = Path(__file__).parent

class TestBasicConfigExtractor(unittest.TestCase):
    def test_get_topology_config_from_xml(self):
        xml_file_path: Path = RESOURCES_PATH.joinpath('resources/test-topology.xml')
        basic_config_extractor: BasicConfigExtractor = BasicConfigExtractor()
        device_counter: dict = {DeviceType.ROUTER: 0, DeviceType.SWITCH: 0}

        result: list[DeviceConfigInfo] = basic_config_extractor.get_topology_config_from_xml(xml_file_path)
        for dev in result:
            device_counter[dev.dev_type] += 1

        assert len(result) == 9, f"Failed to parse xml - invalid number of devices found: 9 != {len(result)}"
        assert device_counter[DeviceType.ROUTER] == 3, f"Routers counter is not equal to 3"
        assert device_counter[DeviceType.SWITCH] == 6, f"Switches counter is not equal to 6"

    def test_get_topology_config_from_xml_raises_exception(self):
        xml_file_path: Path = RESOURCES_PATH.joinpath('resources/non-existent-topology.xml')
        basic_config_extractor: BasicConfigExtractor = BasicConfigExtractor()
        self.assertRaises(XmlOpenException, basic_config_extractor.get_topology_config_from_xml, xml_file_path)


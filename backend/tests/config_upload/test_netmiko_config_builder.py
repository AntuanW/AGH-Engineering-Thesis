import unittest
from pathlib import Path

from app.config_upload.netmiko_config_builder import NetmikoConfigBuilder
from app.running_config.basic_config_extractor import BasicConfigExtractor
from app.running_config.util.device_config_types import DeviceConfigInfo

RESOURCES_PATH = Path(__file__).parent


class TestNetmikoConfigBuilder(unittest.TestCase):
    def test_get_commands(self):
        xml_file_path: Path = RESOURCES_PATH.joinpath('resources/test-topology.xml')
        basic_config_extractor: BasicConfigExtractor = BasicConfigExtractor()
        netmiko_config_builder: NetmikoConfigBuilder = NetmikoConfigBuilder()

        device_config_info_list: list[DeviceConfigInfo] = basic_config_extractor.get_topology_config_from_xml(
            xml_file_path)
        device_running_config_0 = device_config_info_list[0].dev_running_config
        config_0 = netmiko_config_builder.get_config(device_running_config_0)
        print(config_0)

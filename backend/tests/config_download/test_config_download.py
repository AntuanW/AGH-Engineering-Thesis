import unittest
from unittest.mock import patch
from app.config_download.config_download_service import ConfigDownloadService
from app.config_download.utils.downloaded_config import DownloadedConfig
from app.models.connection import ConnectionModel
from app.common.netmiko.netmiko_client import NetmikoClient
from app.common.netmiko.netmiko_device import NetmikoDevice
from app.config_download.utils.download_config_request import DownloadConfigRequest
from app.running_config.util.device_config_types import DeviceType
import tests.config_download.mocked_method_results as mmr


class TestConfigDownloadService(unittest.TestCase):
    @patch("app.common.netmiko.netmiko_client.NetmikoClient")
    def test_parse_neighbors_regular_case(self, netmiko_client_mock):
        origin_name = "Hostname"
        expected_output = [
            ConnectionModel(
                origin_name=origin_name,
                neighbour_name="Router",
                from_interface="Fas 0/1",
                to_interface="Gig 0/0/1",
            ),
            ConnectionModel(
                origin_name=origin_name,
                neighbour_name="Switch",
                from_interface="Fas 0/3",
                to_interface="Gig 0/0/1",
            )
        ]
        config_download = ConfigDownloadService(netmiko_client_mock)

        result: list[ConnectionModel] = config_download._parse_neighbors(mmr.CDP_OUTPUT_REGULAR_CASE, origin_name)


        assert len(result) == len(expected_output)
        assert result[0].neighbour_name == expected_output[0].neighbour_name
        assert result[0].from_interface == expected_output[0].from_interface
        assert result[0].to_interface == expected_output[0].to_interface
        assert result[1].neighbour_name == expected_output[1].neighbour_name
        assert result[1].from_interface == expected_output[1].from_interface
        assert result[1].to_interface == expected_output[1].to_interface

    @patch("app.common.netmiko.netmiko_client.NetmikoClient")
    def test_parse_neighbors_with_merged_last_two_columns(self, netmiko_client_mock):
        origin_name = "Hostname"
        expected_output = [
            ConnectionModel(
                origin_name=origin_name,
                neighbour_name="Router",
                from_interface="Fas 0/1",
                to_interface="Gig 0/0/1",
            ),
            ConnectionModel(
                origin_name=origin_name,
                neighbour_name="Switch",
                from_interface="Fas 0/3",
                to_interface="Gig 0/0/1",
            )
        ]
        config_download = ConfigDownloadService(netmiko_client_mock)

        result: list[ConnectionModel] = config_download._parse_neighbors(mmr.CDP_OUTPUT_WITH_MERGED_LAST_COLUMNS, origin_name)

        assert len(result) == len(expected_output)
        assert result[0].neighbour_name == expected_output[0].neighbour_name
        assert result[0].from_interface == expected_output[0].from_interface
        assert result[0].to_interface == expected_output[0].to_interface
        assert result[1].neighbour_name == expected_output[1].neighbour_name
        assert result[1].from_interface == expected_output[1].from_interface, f"{result[1].from_interface}"
        assert result[1].to_interface == expected_output[1].to_interface

    @patch("app.common.netmiko.netmiko_client.NetmikoClient")
    def test_download_config_from_device(self, netmiko_client_mock: NetmikoClient):
        devices_list = [
            NetmikoDevice(ip_address="1.1.1.1", port=0),
            NetmikoDevice(ip_address="2.2.2.2", port=1)
        ]
        download_config_request: DownloadConfigRequest = DownloadConfigRequest(
            lab_name="test_lab",
            lab_group="1",
            devices=devices_list
        )
        mocked_netmiko_output_router = (
            mmr.ROUTER_CONFIG,
            mmr.CDP_OUTPUT_ROUTER,
            mmr.ROUTER_HOSTNAME,
            mmr.ROUTER_VERSION
        )
        mocked_netmiko_output_switch = (
            mmr.SWITCH_CONFIG,
            mmr.CDP_OUTPUT_SWITCH,
            mmr.SWITCH_HOSTNAME,
            mmr.SWITCH_VERSION
        )
        netmiko_client_mock.download_config_from_device.side_effect = [mocked_netmiko_output_router,
                                                                       mocked_netmiko_output_switch]

        config_download_service = ConfigDownloadService(netmiko_client_mock)
        result: list[DownloadedConfig] = config_download_service.download_devices_config(download_config_request)

        print(result[0].name)
        assert len(result) == 2
        assert result[0].name == "Router", str(result[0].name)
        assert result[0].device_type == DeviceType.ROUTER
        assert len(result[0].neighbours) == 1
        assert result[1].name == "Switch"
        assert result[1].device_type == DeviceType.SWITCH
        assert len(result[1].neighbours) == 1

    @patch("app.common.netmiko.netmiko_client.NetmikoClient")
    def test_strip_hostname(self, netmiko_client_mock):
        test_prompt_1 = "Router#"
        test_prompt_2 = "Router(config)#"
        test_prompt_3 = "Router(config-router)#"
        test_prompt_4 = "Router(config-if)#"
        expected_hostname = "Router"

        config_download = ConfigDownloadService(netmiko_client_mock)

        assert config_download._strip_hostname(test_prompt_1) == expected_hostname
        assert config_download._strip_hostname(test_prompt_2) == expected_hostname
        assert config_download._strip_hostname(test_prompt_3) == expected_hostname
        assert config_download._strip_hostname(test_prompt_4) == expected_hostname
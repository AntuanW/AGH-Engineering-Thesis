import unittest
from unittest.mock import MagicMock

from app.config_download.utils.downloaded_config import DownloadedConfig
from app.instruction_export.home_instruction_export_service import HomeInstructionExportService
from app.running_config.util.device_config_types import DeviceType

config = """!
version 15.1
no service timestamps log datetime msec
no service timestamps debug datetime msec
no service password-encryption
!
hostname Router
!
!
!
!
!
!
!
!
ip cef
no ipv6 cef
!
!
!
!
license udi pid CISCO2911/K9 sn FTX15249Q72-
!
!
!
!
!
!
!
!
!
!
!
spanning-tree mode pvst
!
!
!
!
!
!
interface GigabitEthernet0/0
no ip address
duplex auto
speed auto
!
interface GigabitEthernet0/0.10
encapsulation dot1Q 10
ip address 100.0.0.1 255.255.255.0
!
interface GigabitEthernet0/0.20
encapsulation dot1Q 20
ip address 200.0.0.2 255.255.255.0
!
interface GigabitEthernet0/1
no ip address
duplex auto
speed auto
shutdown
!
interface GigabitEthernet0/2
no ip address
duplex auto
speed auto
shutdown
!
interface Vlan1
no ip address
shutdown
!
ip classless
!
ip flow-export version 9
!
!
!
!
!
!
!
line con 0
!
line aux 0
!
line vty 0 4
login
!
!
!
end"""

class TestHomeInstructionExportService(unittest.TestCase):
    def test_export_instruction(self):
        mock_downloaded_config = DownloadedConfig(
            name="R11",
            device_type=DeviceType.ROUTER,
            neighbours=[],
            config=config
        )
        pdf_generator_mock = MagicMock()
        pdf_generator_mock.generate_pdf.return_value = ""
        pdf_generator_mock.filename.return_value = "test"

        download_results = [mock_downloaded_config]

        home_instruction_export_service = HomeInstructionExportService(pdf_generator=pdf_generator_mock)
        filename = home_instruction_export_service.export_instruction(download_results)
        self.assertTrue(filename)

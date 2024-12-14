import unittest
from unittest.mock import MagicMock

from app.config_download.utils.downloaded_config import DownloadedConfig
from app.instruction_export.home_instruction_export_service import HomeInstructionExportService
from app.running_config.util.device_config_types import DeviceType


class TestHomeInstructionExportService(unittest.TestCase):
    def test_export_instruction(self):
        mock_downloaded_config = DownloadedConfig(
            name="R11",
            device_type=DeviceType.ROUTER,
            neighbours=[],
            config="interface GigabitEthernet0/0 ip address 192.168.1.1 255.255.255.0 no shutdown"
        )
        pdf_generator_mock = MagicMock()
        pdf_generator_mock.generate_pdf.return_value = ""
        pdf_generator_mock.filename.return_value = "test"

        download_results = [mock_downloaded_config]

        home_instruction_export_service = HomeInstructionExportService(pdf_generator=pdf_generator_mock)
        filename = home_instruction_export_service.export_instruction(download_results)
        self.assertTrue(filename)

import unittest

from pydantic import IPvAnyAddress

from app.config_upload.util.netmiko_types import NetmikoDeviceType
from app.models.connection import ConnectionModel
from app.student_instruction_export.student_instruction_export_service import InstructionExportService
from app.models.mapping import MappingModel
from app.models.mapped_device import MappedDeviceModel


class TestStudentInstructionExportService(unittest.TestCase):
    def test_export_instructions(self):
        mock_mappings = [
            MappingModel(lab_group=1, mapped_devices=[
                MappedDeviceModel(
                    name='R11',
                    netmiko_device_type=NetmikoDeviceType('cisco_ios'),
                    ip_address=IPvAnyAddress('172.17.145.10'),
                    port=2001,
                    neighbours=[
                        ConnectionModel(
                            neighbour_name='R12',
                            from_interface='GigabitEthernet0/0',
                            to_interface='GigabitEthernet0/0',
                        )
                    ],
                    mapped_config=['show version', 'show running-config'],
                ),
                MappedDeviceModel(
                    name='R12',
                    netmiko_device_type=NetmikoDeviceType('cisco_ios'),
                    ip_address=IPvAnyAddress('172.17.145.10'),
                    port=2002,
                    neighbours=[
                        ConnectionModel(
                            neighbour_name='R11',
                            from_interface='GigabitEthernet0/0',
                            to_interface='GigabitEthernet0/0',
                        )
                    ],
                    mapped_config=['show version', 'show running-config'],
                ),
            ]),
            MappingModel(lab_group=2, mapped_devices=[
                MappedDeviceModel(
                    name='R21',
                    netmiko_device_type=NetmikoDeviceType('cisco_ios'),
                    ip_address=IPvAnyAddress('172.17.145.10'),
                    port=2001,
                    neighbours=[
                        ConnectionModel(
                            neighbour_name='R22',
                            from_interface='GigabitEthernet0/0',
                            to_interface='GigabitEthernet0/0',
                        )
                    ],
                    mapped_config=['show version', 'show running-config'],
                ),
                MappedDeviceModel(
                    name='R22',
                    netmiko_device_type=NetmikoDeviceType('cisco_ios'),
                    ip_address=IPvAnyAddress('172.17.145.10'),
                    port=2002,
                    neighbours=[
                        ConnectionModel(
                            neighbour_name='R21',
                            from_interface='GigabitEthernet0/0',
                            to_interface='GigabitEthernet0/0',
                        )
                    ],
                    mapped_config=['show version', 'show running-config'],
                ),
            ])
        ]

        instruction_export_service = InstructionExportService()
        instruction_export_service.export_instructions(mock_mappings)
        assert True

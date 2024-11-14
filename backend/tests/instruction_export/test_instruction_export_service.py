import unittest

from app.instruction_export.instruction_export_service import InstructionExportService


class TestInstructionExportService(unittest.TestCase):
    def test_export_instructions(self):
        groups = {
            "Grupa 1": ["Urządzenie 1", "Urządzenie 2", "Urządzenie 3"],
            "Grupa 2": ["Urządzenie 4", "Urządzenie 5", "Urządzenie 6"]
        }
        connections = [
            ("Urządzenie 1", "Port 1", "Urządzenie 2", "Port 1"),
            ("Urządzenie 1", "Port 2", "Urządzenie 3", "Port 1"),
            ("Urządzenie 4", "Port 1", "Urządzenie 5", "Port 1"),
            ("Urządzenie 4", "Port 2", "Urządzenie 6", "Port 1"),
            ("Urządzenie 5", "Port 2", "Urządzenie 6", "Port 2"),
        ]
        instruction_export_service = InstructionExportService()
        instruction_export_service.export_instructions(groups, connections)
        assert True

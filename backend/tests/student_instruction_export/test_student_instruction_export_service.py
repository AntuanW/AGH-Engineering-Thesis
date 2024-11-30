import unittest

from app.repository.mapping_repository import MappingRepository
from app.student_instruction_export.student_instruction_export_service import StudentInstructionExportService


class TestStudentInstructionExportService(unittest.TestCase):
    def test_export_instructions(self):
        mapping_repo = MappingRepository()
        mappings = mapping_repo.find_objects({})
        instruction_export_service = StudentInstructionExportService()
        filename = instruction_export_service.export_instructions(mappings)
        self.assertTrue(filename)

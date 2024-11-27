import unittest
from unittest.mock import MagicMock

from app.student_instruction_export.student_instruction_pdf_generator import InstructionPdfGenerator


class TestStudentInstructionPdfGenerator(unittest.TestCase):
    def test_generate_pdf(self):

        instruction_pdf_generator = InstructionPdfGenerator()
        instruction_pdf_generator.generate_pdf()
        assert True

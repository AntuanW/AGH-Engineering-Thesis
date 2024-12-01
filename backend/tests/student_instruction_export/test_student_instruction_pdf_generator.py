import unittest

from app.student_instruction_export.student_instruction_pdf_generator import StudentInstructionPdfGenerator
from reportlab.platypus import Paragraph


class TestStudentInstructionPdfGenerator(unittest.TestCase):
    def test_generate_pdf(self):
        content = [Paragraph("TEST")]
        instruction_pdf_generator = StudentInstructionPdfGenerator()
        instruction_pdf_generator.generate_pdf(content)
        self.assertTrue(instruction_pdf_generator.filename)

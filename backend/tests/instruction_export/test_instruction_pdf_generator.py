import unittest

from app.instruction_export.util.instruction_pdf_generator import InstructionPdfGenerator

class TestInstructionPdfGenerator(unittest.TestCase):
    def test_generate_pdf(self):
        instruction_pdf_generator = InstructionPdfGenerator()
        instruction_pdf_generator.generate_pdf()
        assert True
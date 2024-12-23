import unittest

from app.pdf_generator.pdf_generator import PdfGenerator
from reportlab.platypus import Paragraph


class TestPdfGenerator(unittest.TestCase):
    def test_generate_pdf(self):
        content = [Paragraph("TEST")]
        instruction_pdf_generator = PdfGenerator()
        filename = instruction_pdf_generator.generate_instruction(content, "test")
        self.assertTrue(filename)

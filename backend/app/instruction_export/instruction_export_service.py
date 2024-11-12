from .util.instruction_pdf_generator import InstructionPdfGenerator


class InstructionExportService:
    def __init__(self):
        self.pdf_generator = InstructionPdfGenerator()

    def export_instructions(self):
        pass

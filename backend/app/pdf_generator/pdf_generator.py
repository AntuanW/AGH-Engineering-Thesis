from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from app.pdf_generator.util.footer_canvas import FooterCanvas
from datetime import datetime
import tempfile
from pathlib import Path


class PdfGenerator:
    TEMP_PATH = Path(tempfile.gettempdir())
    PDF_OUTPUT_DIR = "pdf_files"

    def generate_instruction(self, content, instruction_type):
        current_datatime = datetime.now()
        filename = f"{instruction_type}_instruction_{current_datatime.strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
        output_dir = self.TEMP_PATH / self.PDF_OUTPUT_DIR

        if not output_dir.exists():
            output_dir.mkdir(parents=True)

        pdfmetrics.registerFont(TTFont('Times New Roman', 'Times.ttf'))
        footer = FooterCanvas(current_datatime)

        doc = BaseDocTemplate(str(output_dir / filename), pagesize=A4)

        frame = Frame(inch, inch, doc.width, doc.height)
        footer_template = PageTemplate(id='header', frames=frame, onPage=footer.on_page)
        doc.addPageTemplates(footer_template)

        doc.build(content)
        return filename

    def generate_lab_instruction(self, content):
        return self.generate_instruction(content, "lab")
    def generate_home_instruction(self, content):
        return self.generate_instruction(content, "home")


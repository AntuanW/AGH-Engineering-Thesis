from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from app.pdf_generator.util.footer_canvas import FooterCanvas
from datetime import datetime
import os


class PdfGenerator:
    def generate_instruction(self, content, instruction_type):
        current_datatime = datetime.now()
        filename = f"{instruction_type}_instruction_{current_datatime.strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
        output_dir = "instruction_export/pdf_files"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        pdfmetrics.registerFont(TTFont('Times New Roman', 'Times.ttf'))
        footer = FooterCanvas(current_datatime)

        doc = BaseDocTemplate(os.path.join(output_dir, filename), pagesize=A4)

        frame = Frame(inch, inch, doc.width, doc.height)
        footer_template = PageTemplate(id='header', frames=frame, onPage=footer.on_page)
        doc.addPageTemplates(footer_template)

        doc.build(content)
        return filename

    def generate_lab_instruction(self, content):
        return self.generate_instruction(content, "lab")
    def generate_home_instruction(self, content):
        return self.generate_instruction(content, "home")


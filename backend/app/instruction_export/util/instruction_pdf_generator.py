from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .footer_canvas import FooterCanvas
from datetime import datetime
import os


class InstructionPdfGenerator:
    def __init__(self):
        self.current_datetime = datetime.now()
        self.filename = f"instruction_{self.current_datetime.strftime('%Y-%m-%d_%H-%M-%S')}.pdf"

    def generate_pdf(self):
        pdfmetrics.registerFont(TTFont('Times New Roman', 'Times.ttf'))
        footer = FooterCanvas(self.current_datetime)

        doc = BaseDocTemplate(os.path.join("pdf_files", self.filename), pagesize=A4)

        frame = Frame(inch, inch, doc.width, doc.height)
        footer_template = PageTemplate(id='header', frames=frame, onPage=footer.on_page)
        doc.addPageTemplates(footer_template)

        main_text_style = ParagraphStyle(
            'Normal',
            parent=getSampleStyleSheet()['Normal'],
            fontName='Times New Roman',
            fontSize=12
        )
        content = [
            Paragraph("To jest przykładowy dokument ze stopką na każdej stronie.", main_text_style),
            Spacer(1, 12),
            PageBreak(),
            Paragraph("To jest przykładowy dokument ze stopką na każdej stronie.", main_text_style),
            Spacer(1, 12),
            PageBreak(),
            Paragraph("To jest przykładowy dokument ze stopką na każdej stronie.", main_text_style),
            Spacer(1, 12)
        ]

        doc.build(content)
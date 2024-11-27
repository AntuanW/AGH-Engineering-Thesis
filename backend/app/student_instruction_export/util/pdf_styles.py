from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class PdfStyles:
    def __init__(self):
        pdfmetrics.registerFont(TTFont('Times New Roman', 'Times.ttf'))
        self.main_style = ParagraphStyle(
            name='Main',
            parent=getSampleStyleSheet()['Normal'],
            fontName='Times New Roman',
            fontSize=12
        )

        self.heading1_style = ParagraphStyle(
            name='Heading1',
            parent=getSampleStyleSheet()['Heading1'],
            fontName='Times New Roman',
            fontSize=20
        )

        self.heading2_style = ParagraphStyle(
            name='Heading2',
            parent=getSampleStyleSheet()['Heading2'],
            fontName='Times New Roman',
            fontSize=16
        )

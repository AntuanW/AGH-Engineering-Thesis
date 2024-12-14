from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.platypus import TableStyle


class PdfStyles:
    def __init__(self):
        pdfmetrics.registerFont(TTFont('Times New Roman', 'Times.ttf'))
        pdfmetrics.registerFont(TTFont('Times New Roman Bold', 'Timesbd.ttf'))
        pdfmetrics.registerFont(TTFont('Times New Roman Italic', 'Timesi.ttf'))
        self.main_style = ParagraphStyle(
            name='Main',
            parent=getSampleStyleSheet()['Normal'],
            fontName='Times New Roman',
            fontSize=12
        )
        self.title_style = ParagraphStyle(
            name='Title',
            parent=getSampleStyleSheet()['Title'],
            fontName='Times New Roman Bold',
            fontSize=24
        )
        self.heading1_style = ParagraphStyle(
            name='Heading1',
            parent=getSampleStyleSheet()['Heading1'],
            fontName='Times New Roman',
            fontSize=20,
        )
        self.heading2_style = ParagraphStyle(
            name='Heading2',
            parent=getSampleStyleSheet()['Heading2'],
            fontName='Times New Roman',
            fontSize=18
        )
        self.italics_style = ParagraphStyle(
            name='Italics',
            parent=getSampleStyleSheet()['Title'],
            fontName='Times New Roman Italic',
            fontSize=16
        )
        self.bullet_style = ParagraphStyle(
            name='Bullet',
            parent=getSampleStyleSheet()['Bullet'],
            fontName='Times New Roman',
            fontSize=12,
            bulletIndent=20,
        )
        self.table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times New Roman Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Times New Roman'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ])

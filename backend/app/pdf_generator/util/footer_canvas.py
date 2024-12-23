from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from pathlib import Path


class FooterCanvas:
    FONTS_DIR_PATH = str(Path(__file__).parent.parent / 'static')

    def __init__(self, current_datetime):
        self.styles = getSampleStyleSheet()
        self.current_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

    def content(self, canvas, doc):
        try:
            pdfmetrics.registerFont(TTFont('Times New Roman', os.path.join(self.FONTS_DIR_PATH, 'Times.ttf')))
        except FileNotFoundError:
            raise FileNotFoundError('Font Times New Roman not found')
        except Exception as e:
            raise Exception(f'Error while registering font Times New Roman: {e}')

        canvas.setFont('Times New Roman', 10)
        page_number_text = f"Strona {doc.page}"
        canvas.drawRightString(A4[0] - inch, 36, page_number_text)
        canvas.drawString(inch, 36, self.current_datetime)

    def on_page(self, canvas, doc):
        self.content(canvas, doc)

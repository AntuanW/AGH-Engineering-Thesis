from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch


class FooterCanvas:
    def __init__(self, current_datetime):
        self.styles = getSampleStyleSheet()
        self.current_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')

    def content(self, canvas, doc):
        canvas.setFont('Times New Roman', 10)
        page_number_text = f"Strona {doc.page}"
        canvas.drawRightString(A4[0] - inch, 36, page_number_text)
        canvas.drawString(inch, 36, self.current_datetime)

    def on_page(self, canvas, doc):
        self.content(canvas, doc)

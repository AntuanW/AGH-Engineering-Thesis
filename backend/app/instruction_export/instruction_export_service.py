from reportlab.platypus import Paragraph, Spacer, PageBreak
from .instruction_pdf_generator import InstructionPdfGenerator
from .util.pdf_styles import PdfStyles


class InstructionExportService:
    def __init__(self):
        self.pdf_generator = InstructionPdfGenerator()
        self.styles = PdfStyles()

    def export_instructions(self, groups, connections):
        content = []
        for group_name, device_name in groups.items():
            content.append(Paragraph("Instrukcja", self.styles.heading1_style))
            content.append(Paragraph(f"Grupa: {group_name}", self.styles.heading1_style))
            content.append(Paragraph(f"Urządzenia: {', '.join(device_name)}", self.styles.heading2_style))
            content.append(Spacer(1, 12))

            filtered_connections = self.filter_connections(device_name, connections)
            formatted_connections = self.format_connections(filtered_connections)
            content.append(Paragraph("Połączenia:", self.styles.heading1_style))
            for connection in formatted_connections:
                content.append(Paragraph(connection, self.styles.main_style))
            content.append(Spacer(1, 12))
            content.append(PageBreak())

        self.pdf_generator.generate_pdf(content)

    def filter_connections(self, devices, connections):
        filtered_connections = [
            connection for connection in connections
            if connection[0] in devices or connection[2] in devices
        ]
        return filtered_connections

    def format_connections(self, connections):
        formatted_connections = []
        for connection in connections:
            device1, port1, device2, port2 = connection
            formatted_connections.append(f"{device1} - {port1} -> {device2} - {port2}")
        return formatted_connections

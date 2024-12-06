from reportlab.platypus import Paragraph, PageBreak, Spacer

from ..models.connection import ConnectionModel
from ..pdf_generator.pdf_generator import PdfGenerator
from ..pdf_generator.util.pdf_styles import PdfStyles
from ..models.mapped_device import MappedDeviceModel


class ConfigPdfExportService:
    def __init__(self, lab_group_number: int):
        self.lab_group_number = lab_group_number
        self.pdf_generator = PdfGenerator(output_dir="configurations", name="configurations", group=lab_group_number)
        self.styles = PdfStyles()

    def export_configurations(self, devices: list[MappedDeviceModel]):
        content = []
        content.append(Paragraph(f"Konfiguracje urządzeń grupy {self.lab_group_number}", self.styles.title_style))
        content.append(Spacer(1, 12))
        for device in devices:
            content.append(Paragraph(f"{device.name}", self.styles.heading1_style))
            content.append(Spacer(1, 12))
            for command in device.mapped_config:
                content.append(Paragraph(f"{command}", self.styles.main_style))
            content.append(PageBreak())

        
        content.append(Paragraph("Schemat:", self.styles.heading1_style))
        content.append(Spacer(1, 12))
        content.append(PageBreak())

        self.pdf_generator.generate_pdf(content)
        return self.pdf_generator.filename

    def _get_names_and_types(self, devices: list[MappedDeviceModel]) -> list[str]:
        return [(device.name, device.device_type) for device in devices]

    def _get_device_connections(self, devices: list[MappedDeviceModel]) -> list[ConnectionModel]:
        connections: set[ConnectionModel] = set()
        for device in devices:
            for connection in device.neighbours:
                if connection not in connections:
                    connections.add(connection)
        return list(connections)

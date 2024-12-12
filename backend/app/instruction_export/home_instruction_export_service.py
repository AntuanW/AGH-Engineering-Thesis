from fastapi import Depends

from reportlab.platypus import Paragraph, Spacer, PageBreak

from app.models.connection import ConnectionModel
from app.pdf_generator.pdf_generator import PdfGenerator
from app.pdf_generator.util.pdf_styles import PdfStyles
from app.config_download.utils.downloaded_config import DownloadedConfig
from app.visualization.topology_visualizer import TopologyVisualizer


class HomeInstructionExportService:
    def __init__(self, pdf_generator=Depends(PdfGenerator)):
        self.pdf_generator: PdfGenerator = pdf_generator
        self.styles = PdfStyles()

    def export_configurations(self, devices: list[DownloadedConfig]) -> str:
        content = []
        content.append(Paragraph("Konfiguracje urządzeń", self.styles.title_style))
        content.append(Spacer(1, 12))
        for device in devices:
            content.append(Paragraph(f"{device.name} - {device.device_type.value}", self.styles.heading1_style))
            content.append(Spacer(1, 12))
            content.append(Paragraph(f"{device.config}", self.styles.main_style))
            content.append(PageBreak())

        devices_types = self._get_device_name_to_type_dict(devices)
        connections = self._get_device_connections(devices)

        visualizer = TopologyVisualizer(devices_types, connections)
        graph = visualizer.generate_graph()
        image = visualizer.draw_graph(graph)
        content.append(Paragraph("Schemat:", self.styles.heading1_style))
        content.append(Spacer(1, 12))
        content.append(image)
        content.append(PageBreak())

        filename = self.pdf_generator.generate_home_instruction(content)
        return filename

    def _get_device_name_to_type_dict(self, devices: list[DownloadedConfig]) -> dict:
        return {device.name: device.device_type for device in devices}

    def _get_device_connections(self, devices: list[DownloadedConfig]) -> list[ConnectionModel]:
        connections: set[ConnectionModel] = set()
        for device in devices:
            for connection in device.neighbours:
                if connection not in connections:
                    connections.add(connection)
        return list(connections)

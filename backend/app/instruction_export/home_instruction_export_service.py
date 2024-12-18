import logging

from fastapi import Depends

from reportlab.platypus import Paragraph, Spacer, PageBreak

from app.common.parsers.instruction_parser import InstructionParser
from app.models.connection import ConnectionModel
from app.pdf_generator.pdf_generator import PdfGenerator
from app.pdf_generator.util.pdf_styles import PdfStyles
from app.config_download.utils.downloaded_config import DownloadedConfig
from app.visualization.topology_visualizer import TopologyVisualizer


class HomeInstructionExportService:
    def __init__(self, pdf_generator=Depends(PdfGenerator)):
        self.pdf_generator: PdfGenerator = pdf_generator
        self.styles = PdfStyles()

    def export_instruction(self, devices: list[DownloadedConfig]) -> str:
        logging.info("Start generating home instruction")
        content = []
        content.extend(self._create_instruction_header())
        for device in devices:
            content.extend(self._create_running_config_section(device))
        content.extend(self._create_topology_graph(devices))

        filename = self.pdf_generator.generate_home_instruction(content)
        logging.info(f"Home instruction successfully generated: {filename}")
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

    def _create_instruction_header(self) -> list[Paragraph]:
        return [
            Paragraph("Running Configi Urządzeń", self.styles.title_style),
            Spacer(1, 12)
        ]

    def _create_running_config_section(self, device: DownloadedConfig) -> list[Paragraph]:
        logging.debug(f"Creating running config section for {device.name}")
        content = [
            Paragraph(f"{device.name} - {device.device_type.value}", self.styles.heading2_style),
            Spacer(1, 12)
        ]

        parsed_configs = InstructionParser.from_source(device.config.split('\n'))
        for parsed_config in parsed_configs:
            content.append(Paragraph(parsed_config, self.styles.main_style))
        content.append(PageBreak())

        return content

    def _create_topology_graph(self, devices: list[DownloadedConfig]) -> list[Paragraph]:
        logging.info("Creating topology schema")
        devices_types = self._get_device_name_to_type_dict(devices)
        connections = self._get_device_connections(devices)

        if not connections:
            logging.warning("No connections found between devices")

        visualizer = TopologyVisualizer(devices_types, connections)
        graph = visualizer.generate_graph()
        image = visualizer.draw_graph(graph)

        return [
            Paragraph("Schemat:", self.styles.heading2_style),
            Spacer(1, 12),
            image
        ]

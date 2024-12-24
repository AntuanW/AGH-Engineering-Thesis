import logging

from reportlab.platypus import Paragraph, Spacer, PageBreak, Table
from app.pdf_generator.pdf_generator import PdfGenerator
from app.pdf_generator.util.pdf_styles import PdfStyles
from ..models.connection import ConnectionModel
from ..models.mapped_device import MappedDeviceModel
from ..models.mapping import MappingCollectionModel
from ..repository.lab_group_repository import LabGroupRepository
from ..running_config.util.device_config_types import DeviceType
from ..visualization.topology_visualizer import TopologyVisualizer

from fastapi import Depends
from bson import ObjectId

from ..repository.topology_repository import TopologyRepository


class LabInstructionExportService:
    def __init__(self,
                 topology_repo = Depends(TopologyRepository),
                 group_repo = Depends(LabGroupRepository),
                 pdf_generator = Depends(PdfGenerator)):
        self.topology_repo: TopologyRepository = topology_repo
        self.group_repo: LabGroupRepository = group_repo
        self.pdf_generator: PdfGenerator = pdf_generator
        self.styles = PdfStyles()

    def export_instructions(self, mapping_collection: MappingCollectionModel) -> str:
        logging.info("Start generating lab instruction")
        content = []
        for group, devices in mapping_collection.mappings.items():
            logging.info(f"Start generating lab instruction for group {group}")
            content.extend(self._create_instruction_header(group, mapping_collection.topology_id))
            content.extend(self._create_connection_steps(devices, group))
            content.extend(self._create_connections_table(devices))
            content.extend(self._create_topology_graph(devices, group))
            logging.info(f"Lab instruction for group {group} successfully generated")

        filename = self.pdf_generator.generate_lab_instruction(content)
        logging.info(f"Lab instruction successfully generated: {filename}")
        return filename

    def _get_device_name_to_type_dict(self, devices: list[MappedDeviceModel]) -> dict:
        return {device.name: device.device_type for device in devices}

    def _get_device_connections(self, devices: list[MappedDeviceModel]) -> list[ConnectionModel]:
        connections: set[ConnectionModel] = set()
        for device in devices:
            for connection in device.neighbours:
                if connection not in connections:
                    connections.add(connection)
        return list(connections)

    def _create_instruction_header(self, group: int, topology_id: str) -> list[Paragraph]:
        topology_name = self.topology_repo.find_object({"_id": ObjectId(topology_id)}).name

        return [
            Paragraph("Instrukcja", self.styles.title_style),
            Paragraph(f"{topology_name}", self.styles.italics_style),
            Spacer(1, 12),
            Paragraph(f"Grupa: {group}", self.styles.heading1_style),
            Spacer(1, 12)
        ]

    def _create_connection_steps(self, devices: list[MappedDeviceModel], group: int) -> list[Paragraph]:
        ip_address = self.group_repo.get_ip_of_group(group)

        content = [
            Paragraph("Aby wgrać konfiguracje, wykonaj następujące kroki:", self.styles.main_style),
            Spacer(1, 12),
            Paragraph("1. Połącz komputer z portem dostępowym.", self.styles.main_style),
            Spacer(1, 6),
            Paragraph(f"2. Podłącz poniższe urządzenia do odpowiednich portów na adresie IP {ip_address}:",
                      self.styles.main_style),
            Spacer(1, 6)
        ]

        for device in devices:
            if device.device_type == DeviceType.PC:
                continue
            content.append(
                Paragraph(f"<bullet>&bull;</bullet> {device.name} - port {device.port}", self.styles.bullet_style))
            content.append(Spacer(1, 6))
        content.append(Spacer(1, 6))

        return content

    def _create_connections_table(self, devices: list[MappedDeviceModel]) -> list[Paragraph]:
        connections = self._get_device_connections(devices)

        data = [["Urządzenie 1", "Interfejs 1", "Urządzenie 2", "Interfejs 2"]]
        data.extend([
            [connection.origin_name, connection.from_interface, connection.neighbour_name, connection.to_interface]
            for connection in connections
        ])
        col_widths = [110, 110, 110, 110]
        table = Table(data, colWidths=col_widths)
        table.setStyle(self.styles.table_style)

        return [
            Paragraph("Tabela połączeń:", self.styles.heading2_style),
            Spacer(1, 12),
            table,
            PageBreak()
        ]

    def _create_topology_graph(self, devices: list[MappedDeviceModel], group: int) -> list[Paragraph]:
        connections = self._get_device_connections(devices)

        if not connections:
            logging.warning("No connections found between devices. Skipping topology schema generation.")
            return [
                Paragraph("Brak schematu!", self.styles.heading2_style)
            ]

        devices_types = self._get_device_name_to_type_dict(devices)

        visualizer = TopologyVisualizer(devices_types, connections)
        graph = visualizer.generate_graph()
        image = visualizer.draw_graph(graph)

        return [
            Paragraph(f"Grupa: {group}", self.styles.heading1_style),
            Paragraph("Schemat:", self.styles.heading2_style),
            Spacer(1, 12),
            image,
            PageBreak()
        ]

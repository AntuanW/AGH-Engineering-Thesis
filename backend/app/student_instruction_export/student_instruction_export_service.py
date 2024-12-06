from reportlab.platypus import Paragraph, Spacer, PageBreak, Table
from .student_instruction_pdf_generator import StudentInstructionPdfGenerator
from .util.pdf_styles import PdfStyles
from ..models.connection import ConnectionModel
from ..models.mapped_device import MappedDeviceModel
from ..models.mapping import MappingModel
from ..visualization.topology_visualizer import TopologyVisualizer

from fastapi import Depends
from bson import ObjectId

from ..repository.topology_repository import TopologyRepository


class StudentInstructionExportService:
    def __init__(self,
                 topology_repo=Depends(TopologyRepository),
                 pdf_generator=Depends(StudentInstructionPdfGenerator)):
        self.topology_repo: TopologyRepository = topology_repo
        self.pdf_generator: StudentInstructionPdfGenerator = pdf_generator
        self.styles = PdfStyles()

    def export_instructions(self, mappings: list[MappingModel]):
        content = []
        for mapping in mappings:
            group = mapping.lab_group_number
            devices = mapping.mapped_devices
            devices_names = self._get_group_devices(devices)
            topology_name = self.topology_repo.find_object({"_id": ObjectId(mapping.topology_id)}).name

            content.append(Paragraph("Instrukcja", self.styles.title_style))
            content.append(Paragraph(f"{topology_name}", self.styles.italics_style))
            content.append(Spacer(1, 12))

            content.append(Paragraph(f"Grupa: {group}", self.styles.heading1_style))
            content.append(Paragraph(f"Urządzenia: {', '.join(devices_names)}", self.styles.heading2_style))
            content.append(Spacer(1, 12))

            data = [["Urządzenie 1", "Interfejs 1", "Urządzenie 2", "Interfejs 2"]]
            connections = self._get_device_connections(devices)
            data.extend([
                [connection.origin_name, connection.from_interface, connection.neighbour_name, connection.to_interface]
                for connection in connections
            ])
            col_widths = [110, 110, 110, 110]
            table = Table(data, colWidths=col_widths)
            table.setStyle(self.styles.table_style)

            content.append(Paragraph("Tabela połączeń:", self.styles.heading1_style))
            content.append(Spacer(1, 12))
            content.append(table)
            content.append(PageBreak())

            devices_types = self._get_device_name_to_type_dict(devices)
            visualizer = TopologyVisualizer(devices_types, connections)
            graph = visualizer.generate_graph()
            image = visualizer.draw_graph(graph)
            content.append(Paragraph(f"Grupa: {group}", self.styles.heading1_style))
            content.append(Paragraph("Schemat:", self.styles.heading1_style))
            content.append(Spacer(1, 12))
            content.append(image)

            content.append(Spacer(1, 12))
            content.append(PageBreak())

        self.pdf_generator.generate_pdf(content)
        return self.pdf_generator.filename

    def _get_group_devices(self, devices: list[MappedDeviceModel]) -> list[str]:
        return sorted([device.name for device in devices])

    def _get_device_name_to_type_dict(self, devices: list[MappedDeviceModel]) -> dict:
        return {device.name: device.device_type for device in devices}

    def _get_device_connections(self, devices: list[MappedDeviceModel]) -> list[ConnectionModel]:
        connections: set[ConnectionModel] = set()
        for device in devices:
            for connection in device.neighbours:
                if connection not in connections:
                    connections.add(connection)
        return list(connections)

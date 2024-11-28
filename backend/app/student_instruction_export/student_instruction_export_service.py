from reportlab.platypus import Paragraph, Spacer, PageBreak
from .student_instruction_pdf_generator import StudentInstructionPdfGenerator
from .util.pdf_styles import PdfStyles
from ..models.mapping import MappingModel


class StudentInstructionExportService:
    def __init__(self):
        self.pdf_generator = StudentInstructionPdfGenerator()
        self.styles = PdfStyles()

    def export_instructions(self, mappings: list[MappingModel]):
        content = []
        for mapping in mappings:
            group = mapping.lab_group
            devices = mapping.mapped_devices
            group_devices = self.get_group_devices(devices)
            content.append(Paragraph("Instrukcja", self.styles.heading1_style))
            content.append(Paragraph(f"Grupa: {group}", self.styles.heading1_style))
            content.append(Paragraph(f"Urządzenia: {', '.join(group_devices)}", self.styles.heading2_style))
            content.append(Spacer(1, 12))

            connections = self.get_device_connections(devices)
            formatted_connections = self.format_connections(connections)
            content.append(Paragraph("Połączenia:", self.styles.heading1_style))
            for connection in formatted_connections:
                content.append(Paragraph(connection, self.styles.main_style))
            content.append(Spacer(1, 12))
            content.append(PageBreak())

        self.pdf_generator.generate_pdf(content)

    def get_group_devices(self, devices):
        result = []
        for device in devices:
            result.append(device.name)
        return result

    def get_device_connections(self, devices):
        connections = set()
        for device in devices:
            for neighbour in device.neighbours:
                connection = (device.name, neighbour.from_interface, neighbour.neighbour_name, neighbour.to_interface)
                reverse_connection = (
                    neighbour.neighbour_name, neighbour.to_interface, device.name, neighbour.from_interface)
                if reverse_connection not in connections:
                    connections.add(connection)
        return list(connections)

    def format_connections(self, connections):
        formatted_connections = []
        for connection in connections:
            device1, port1, device2, port2 = connection
            formatted_connections.append(f"{device1} - {port1} -> {device2} - {port2}")
        return formatted_connections

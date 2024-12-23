import os
import unittest
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Spacer

from app.visualization.topology_visualizer import TopologyVisualizer
from app.models.connection import ConnectionModel


class TestTopologyVisualizer(unittest.TestCase):
    PDF_FILENAME = "pdf_files/test_topology_visualization.pdf"

    def setUp(self):
        if os.path.exists(self.PDF_FILENAME):
            os.remove(self.PDF_FILENAME)

    def generate_pdf_with_image(self, image):
        doc = SimpleDocTemplate(self.PDF_FILENAME, pagesize=A4)

        content = [image, Spacer(1, 12)]
        doc.build(content)

    def test_draw_graph(self):
        devices = {'S11': 'SWITCH', 'S12': 'SWITCH', 'S13': 'SWITCH', 'R11': 'ROUTER', 'R12': 'ROUTER', 'R13': 'ROUTER',
                   'R14': 'ROUTER'}
        connections = [
            ConnectionModel(origin_name='S11', neighbour_name='R11', from_interface='FastEthernet0/0',
                            to_interface='GigabitEthernet0/1/1'),
            ConnectionModel(origin_name='S12', neighbour_name='R12', from_interface='FastEthernet0/0',
                            to_interface='GigabitEthernet0/1'),
            ConnectionModel(origin_name='S13', neighbour_name='R13', from_interface='FastEthernet0/0',
                            to_interface='GigabitEthernet0/1'),
            ConnectionModel(origin_name='R11', neighbour_name='S13', from_interface='GigabitEthernet0/0',
                            to_interface='FastEthernet0/1'),
            ConnectionModel(origin_name='R12', neighbour_name='S13', from_interface='GigabitEthernet0/0',
                            to_interface='FastEthernet0/2'),
            ConnectionModel(origin_name='R13', neighbour_name='S11', from_interface='GigabitEthernet0/0',
                            to_interface='FastEthernet0/1'),
            ConnectionModel(origin_name='R14', neighbour_name='S11', from_interface='GigabitEthernet0/0',
                            to_interface='FastEthernet0/2'),

        ]

        visualizer = TopologyVisualizer(devices, connections)
        graph = visualizer.generate_graph()
        image = visualizer.draw_graph(graph)
        self.generate_pdf_with_image(image)

        assert os.path.isfile(self.PDF_FILENAME)

    def test_draw_graph_pc(self):
        devices = {'S11': 'SWITCH', 'S12': 'SWITCH', 'S13': 'SWITCH', 'R11': 'ROUTER', 'K11': 'PC', 'K12': 'PC'}

        connections = [
            ConnectionModel(origin_name='S11', neighbour_name='R11', from_interface='FastEthernet0/3',
                            to_interface='GigabitEthernet0/0/0'),
            ConnectionModel(origin_name='S11', neighbour_name='S12', from_interface='FastEthernet0/1',
                            to_interface='FastEthernet0/1'),
            ConnectionModel(origin_name='S11', neighbour_name='S13', from_interface='FastEthernet0/2',
                            to_interface='FastEthernet0/1'),
            ConnectionModel(origin_name='S12', neighbour_name='K11', from_interface='FastEthernet0/2',
                            to_interface='PC0'),
            ConnectionModel(origin_name='S13', neighbour_name='K12', from_interface='FastEthernet0/2',
                            to_interface='PC0'),
        ]

        visualizer = TopologyVisualizer(devices, connections)
        graph = visualizer.generate_graph()
        image = visualizer.draw_graph(graph)
        self.generate_pdf_with_image(image)

        assert os.path.isfile(self.PDF_FILENAME)

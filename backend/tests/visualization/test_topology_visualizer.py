import unittest

from app.visualization.topology_visualizer import TopologyVisualizer
from app.models.connection import ConnectionModel


class TestTopologyVisualizer(unittest.TestCase):
    def test_draw_graph(self):
        devices = ['S11', 'S12', 'S13', 'R11', 'R12', 'R13', 'R14']
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
        graph = visualizer._generate_graph()
        image = visualizer.draw_graph(graph)
        image.show()

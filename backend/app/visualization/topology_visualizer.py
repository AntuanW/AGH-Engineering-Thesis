import networkx as nx
from reportlab.platypus import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import PIL
import matplotlib.pyplot as plt
from io import BytesIO
import os

from app.models.connection import ConnectionModel
from app.running_config.util.device_config_types import DeviceType


def shorten_interface_name(interface_name: str) -> str:
    if interface_name.startswith("GigabitEthernet"):
        return "GE" + interface_name[15:]
    elif interface_name.startswith("FastEthernet"):
        return "FE" + interface_name[12:]
    elif interface_name.startswith("TenGigabitEthernet"):
        return "TE" + interface_name[18:]
    else:
        return interface_name


class TopologyVisualizer:
    def __init__(self, devices: dict, connections: list[ConnectionModel]):
        self.devices = devices
        self.connections = connections
        self.icons = {
            'switch': os.path.join(os.path.dirname(__file__), "icons", "switch.jpg"),
            'router': os.path.join(os.path.dirname(__file__), "icons", "router.jpg"),
            'pc': os.path.join(os.path.dirname(__file__), "icons", "pc.jpg")
        }
        self.images = {}
        try:
            self.images['switch'] = PIL.Image.open(self.icons['switch'])
            self.images['router'] = PIL.Image.open(self.icons['router'])
            self.images['pc'] = PIL.Image.open(self.icons['pc'])
        except Exception as e:
            raise FileNotFoundError("One or more device images could not be loaded.")

    def draw_graph(self, graph: nx.Graph) -> Image:
        pos = nx.kamada_kawai_layout(graph)

        for edge in list(graph.edges):
            node1, node2 = edge
            if "link_" in node1:
                trap_node, main_node = node1, node2
            elif "link_" in node2:
                trap_node, main_node = node2, node1
            else:
                continue

            neighbours = list(graph.neighbors(trap_node))
            if len(neighbours) == 2:
                origin, neighbour = neighbours
                x_origin, y_origin = pos[origin]
                x_neighbour, y_neighbour = pos[neighbour]
                pos[trap_node] = ((x_origin + x_neighbour) / 2, (y_origin + y_neighbour) / 2)

        fig, ax = plt.subplots(figsize=(10, 10))
        tr_figure = ax.transData.transform
        tr_axes = fig.transFigure.inverted().transform

        icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.05
        icon_center = icon_size / 2.0

        nx.draw(graph, pos, with_labels=False, node_size=0, edge_color='black', width=2)

        for node in graph.nodes:
            if graph.nodes[node]['image'] is None:
                continue
            xf, yf = tr_figure(pos[node])
            xa, ya = tr_axes((xf, yf))
            a = plt.axes((xa - icon_center, ya - icon_center, icon_size, icon_size))
            a.imshow(graph.nodes[node]['image'])
            a.axis('off')
            a.text(xa + 15, ya - 16, node, fontsize=10,
                   bbox=dict(facecolor='white', edgecolor='none', boxstyle='square'))

        edge_labels = nx.get_edge_attributes(graph, 'label')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, label_pos=0.65, font_size=8, ax=ax)

        buffer = BytesIO()
        plt.savefig(buffer, format="png", bbox_inches="tight")
        plt.close(fig)
        buffer.seek(0)

        return Image(buffer, width=A4[0] - 2 * inch, height=A4[0] - 2 * inch)

    def generate_graph(self) -> nx.Graph:
        graph = nx.Graph()
        for device_name, device_type in self.devices.items():
            if device_type == DeviceType.SWITCH:
                graph.add_node(device_name, image=self.images['switch'])
            elif device_type == DeviceType.ROUTER:
                graph.add_node(device_name, image=self.images['router'])
            else:
                graph.add_node(device_name, image=self.images['pc'])

        for i, connection in enumerate(self.connections):
            from_interface = shorten_interface_name(connection.from_interface)
            to_interface = shorten_interface_name(connection.to_interface)

            new_node = f"link_{i}"
            graph.add_node(new_node, image=None)

            graph.add_edge(connection.origin_name, new_node, label=from_interface)
            graph.add_edge(new_node, connection.neighbour_name, label=to_interface)

        return graph

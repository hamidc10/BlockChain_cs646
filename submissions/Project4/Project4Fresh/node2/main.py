from src.node import Node
from src.constants import node1_port, node2_port, node3_port

node2 = Node(
    folder="node2",
    socket_port=node2_port,
    other_node_folders=["node1", "node3"],
    other_node_socket_ports=[node1_port, node3_port],
)
node2.run()

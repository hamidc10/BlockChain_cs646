from src.node import Node
from src.constants import node1_port, node2_port, node3_port

node3 = Node(
    folder="node3",
    socket_port=node3_port,
    other_node_folders=["node1", "node2"],
    other_node_socket_ports=[node1_port, node2_port],
)
node3.run()

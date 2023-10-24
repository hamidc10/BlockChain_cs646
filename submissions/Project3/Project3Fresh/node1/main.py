from src.node import Node
from src.constants import node1_port, node2_port, node3_port

node1 = Node(
    folder="node1",
    socket_port=node1_port,
    other_node_socket_ports=[node2_port, node3_port],
)
node1.run()

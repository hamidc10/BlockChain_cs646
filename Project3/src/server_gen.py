import threading
import os
import shutil
import socket
from constants import server_skeleton

def init_nodes():
    Nodes_folder = ["Node1", "Node2", "Node3"]
    for node in Nodes_folder:
        os.makedirs(node, exist_ok=True)
        shutil.copy(server_skeleton, f"{node}/server.py")
    main(ports)

ports = [1001, 1002, 1003]  # Unique ports for each server

def server_start(node_folder, port):
    server_module = f"{node_folder}.server"
    server = __import__(server_module, fromlist=['Server'])
    server_call = server.Server(port)
    server_call.run()

def main(ports):
    threads = []
    for i, node_folder in enumerate(["Node1", "Node2", "Node3"]):
        t = threading.Thread(target=server_start, args=(node_folder, ports[i]))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    init_nodes()
import threading
import os
import shutil
from constants import  client_skeleton

def init_nodes():
    Nodes_folder = ["Node1", "Node2", "Node3"]
    for node in Nodes_folder:
        os.makedirs(node, exist_ok=True)
        shutil.copy(client_skeleton, f"{node}/client.py")      
    main(ports)

ports = [1001, 1002, 1003]
#Used this to help me with simplifying the names of the imports
#https://www.programiz.com/python-programming/methods/built-in/__import__
def client_start(node_folder, port):
    client_node = f"{node_folder}.client"
    client = __import__(client_node, fromlist=['Client'])
    client_call = client.Client(port)
    client_call.run()
    
#Used to help with threading
#https://www.codecademy.com/resources/docs/python/threading/thread
#https://docs.python.org/3/library/threading.html
#https://www.geeksforgeeks.org/joining-threads-in-python/
def main(ports):
    threads = []
    for i, node_folder in enumerate(["Node1", "Node2", "Node3"]):
        t = threading.Thread(target=client_start, args=(node_folder, ports[i]))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

if __name__ == "__main__":
    init_nodes()
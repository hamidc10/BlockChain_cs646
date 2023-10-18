import socket
import threading


class Server:
    def __init__(self, port: int):
        self.port=port
        
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = ("127.0.0.1", self.port)
        s.bind(server)
        s.listen(5)
        while True:
            clientsocket,addres =s.accept()
            print(f"Connected to port {self.port}")




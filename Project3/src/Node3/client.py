import socket


class Client:
    def __init__(self,port:int):
        self.port=port
        
    def run(self):
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(("127.0.0.1",self.port))
        

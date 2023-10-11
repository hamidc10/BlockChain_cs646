#code that establishes connection.
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#server we want client to connect to
server = ("127.0.0.1",5555)
s.connect(server)

#closes connection
s.close()
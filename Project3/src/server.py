# application that hosts connection
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# what ip/port we want the server to be on
server = ("127.0.0.1",5555)
s.bind(server)

#establishes how many connections we want the server to listen for
s.listen(5)

# loop to keep connection going
while True:
    clientsocket, address = s.accept()
    print ("connection from " + str(address) + " has been established!")
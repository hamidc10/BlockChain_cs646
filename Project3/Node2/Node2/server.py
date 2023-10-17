# application that hosts connection
import socket
import os

file_size = os.path.getsize("Node2Comms.txt")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# what ip/port we want the server to be on
server = ("127.0.0.1",5556)
s.bind(server)
#establishes how many connections we want the server to listen for
s.listen(5)

# loop to keep connection going
while True:
    clientsocket, address = s.accept()
    print ("connection from " + str(address) + " has been established!")

    clientsocket.send(b"Connection Established")

    my_message =clientsocket.recv(100)
    print(my_message.decode("UTF-8"))

    clientsocket.send(str(file_size).encode())

    f = open("myfile.txt","rb")
    content = f.read()
    f.close()
    clientsocket.send(content)
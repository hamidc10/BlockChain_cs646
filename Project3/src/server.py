# application that hosts connection
import socket
import os

file_size = os.path.getsize("myfile.txt")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# what ip/port we want the server to be on
server = ("127.0.0.1",5555)
s.bind(server)

#establishes how many connections we want the server to listen for
s.listen(5)

# loop to keep connection going and send messages, should expand on this potentially to have communications between nodes?
while True:
    clientsocket, address = s.accept()
    print ("connection from " + str(address) + " has been established!")

    clientsocket.send(b"Connection Established")

    my_message = clientsocket.recv(100)
    print(my_message.decode("UTF-8)"))

    my_message = clientsocket.recv(100)
    print(my_message.decode("UTF-8"))
    
    clientsocket.send(str(file_size).encode())


    #clientsocket.send(b"Goodbye")
    f = open("myfile.txt", "rb")
    content = f.read()
    f.close()
    clientsocket.send(content)

# need to set up error handling so that way we do not keep getting "address in use" errors.
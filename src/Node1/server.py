import socket
import os

peers = [("127.0.0.1",5556),("127.0.0.1",5557)]

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server =("127.0.0.1",5555)
s.bind(server)
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print("Connection From " + str(address) + " established")

    clientsocket.send(b"Connection Established")

    my_message = clientsocket.recv(100)
    print(my_message.decode("UTF-8"))
    clientsocket.send(b'OK')
    

    my_message = clientsocket.recv(int(my_message))

    if os.path.isfile("temp.txt"):
        print("file already present")
    else:
        f=open("temp.txt","wb")
        f.write(my_message)
        f.close()


        for p in peers:
            p2p = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            print(p)
            p2p.connect(p)
            response = p2p.recv(100)
            print(response.decode("UTF-8"))

        
            file_size = os.path.getsize("temp.txt")
            p2p.send(str(file_size).encode())


            response = p2p.recv(100)
            print(response)
            p2p.send(my_message)
        
            p2p.close()
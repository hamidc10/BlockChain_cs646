import os
import socket

def sendMessage(filename):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("127.0.0.1",5555))
    response = s.recv(100)
    print(response.decode("UTF-8"))

    
    f = open(filename,"rb")
    content=f.read()
    f.close()
    
    file_size = os.path.getsize(filename)
    s.send(str(file_size).encode())


    response = s.recv(100)
    print(response)
    s.send(content)
    
    s.close()

sendMessage("Newfile.txt")
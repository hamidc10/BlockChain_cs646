#code that establishes connection.
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#server we want client to connect to

# Should set this up so it can be implemented in each node i believe? 


server = ("127.0.0.1",5555)
s.connect(server)
response = s.recv(100)
print(response.decode("UFT-8"))

message = "Test"
message = message.encode()
s.send(message)

response = s.recv(100)
my_size = int(response)


content = s.recv(my_size)
f = open("Newfile.txt", "wb")
f.write(content)
f.close()
#print(response.decode("UTF-8"))

#closes connection
s.close()
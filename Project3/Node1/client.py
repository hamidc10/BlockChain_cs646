#code that establishes connection.
#Important note you have to delete the terminal 
#then new terminal when you stop the connection of the server to client.
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#server we want client to connect to
# server = ("127.0.0.1",5555)
# s.connect(server)
s.connect(("127.0.0.1",5555))
response = s.recv(100)
print(response.decode("UTF-8"))

message = "Test"
message = message.encode()
s.send(message)

response = s.recv(100)
my_size = int(response)

content = s.recv(my_size)

f = open("Node1Comms.txt", "wb")
f.write(content)
f.close()


s.close()
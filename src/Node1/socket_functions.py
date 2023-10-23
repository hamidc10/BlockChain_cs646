import os
import socket

import constants

"""
Blockchain socket communication protocol (work in progress)

For syncing transactions and blocks between nodes

The primary node acts as a server and opens a socket to send transactions and blocks to secondary nodes.
The secondary nodes connect to the primary node socket to receive the transactions and blocks.

Each block/transaction file is sent using the following 3-part message protocol:
1. Send the file type as a message ("TRANSACTION" or "BLOCK")
2. Send the file name as a message (so the client knows what to save it as)
3. Send the file content as a message

Each message is made up of 4 sends/receives on the socket:
1. The server sends the message size (so the client knows how big of a buffer to use)
2. The client confirms that it received the message size
3. The server sends the message content
4. The client confirms that it received the message content

Connection logs are saved to socket_server.log and socket_client.log files.
"""

socket_ip = "127.0.0.1"
server_socket_port = 5558
server_socket_address = (socket_ip, server_socket_port)


### LOG FUNCTIONS


def log(log_file_name: str, message: str):
    with open(log_file_name, "a") as f:
        f.write(message + "\n")


def server_socket_log(message: str):
    log("socket_server.log", message)


def client_socket_log(message: str):
    log("socket_client.log", message)


### INITIAL CONNECTION FUNCTIONS


# Used by the primary node to open a socket for communication with secondary nodes
def open_server_socket() -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_socket_address)
    server_socket.listen()
    return server_socket


# Used by secondary nodes to connect to the primary node
def connect_to_server_socket() -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(server_socket_address)
    client_socket_log(f"Connected to server {server_socket_address}")
    return server_socket


# Used by the primary node to accept a connection from a secondary node
def connect_to_client_socket(server_socket: socket.socket) -> socket.socket:
    client_socket, address = server_socket.accept()
    server_socket_log(f"Connected to client {address}")
    return client_socket


# Used by the primary node to accept a connection from a secondary node
def connect_to_peer(peer_socket: socket.socket) -> socket.socket:
    p2p_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p2p_socket.connect(peer_socket)
    client_socket_log(f"Connected to peer {peer_socket}")
    return p2p_socket


### MESSAGE HELPER FUNCTIONS


def send_message(client_socket: socket.socket, message: bytes):
    # send size
    client_socket.send(str(len(message)).encode())

    # confirm size was received
    response = client_socket.recv(100)
    if response != b"SIZE RECEIVED":
        raise IOError

    # send message
    client_socket.send(message)

    # confirm message was received
    response = client_socket.recv(100)
    if response != b"MESSAGE RECEIVED":
        raise IOError


def receive_message(server_socket: socket.socket) -> bytes:
    # receive size
    response = server_socket.recv(100)
    size = int(response)

    # confirm size was received
    server_socket.send(b"SIZE RECEIVED")

    # receive message
    response = server_socket.recv(size)

    # confirm message was received
    server_socket.send(b"MESSAGE RECEIVED")

    return response


### FILE FUNCTIONS


def send_file(
    client_socket: socket.socket,
    file_type: str,
    file_name: str,
    file_path: str,
):
    # send file type
    send_message(client_socket, file_type.encode())

    # send file name
    send_message(client_socket, file_name.encode())

    # read file content
    with open(file_path, "rb") as f:
        content = f.read()

    # send file content
    send_message(client_socket, content)


# The primary node will use this to send transactions to the secondary nodes
def send_transaction_file(
    client_socket: socket.socket,
    file_name: str,
    file_path: str,
):
    send_file(client_socket, "TRANSACTION", file_name, file_path)
    server_socket_log(f"Sent TRANSACTION file {file_name} to client from {file_path}")


# The primary node will use this to send transactions to the secondary nodes
def send_verified_transaction_file(
    client_socket: socket.socket,
    file_name: str,
    file_path: str,
):
    send_file(client_socket, "TRANSACTION_VERIFIED", file_name, file_path)
    server_socket_log(
        f"Sent TRANSACTION_VERIFIED file {file_name} to client from {file_path}"
    )


# The primary node will use this to send blocks to the secondary nodes
def send_block_file(
    client_socket: socket.socket,
    file_name: str,
    file_path: str,
):
    send_file(client_socket, "BLOCK", file_name, file_path)
    server_socket_log(f"Sent BLOCK file {file_name} to client from {file_path}")


# Secondary nodes will use this to receive transactions and blocks from the primary node
def receive_file(server_socket: socket.socket):
    # receive file type
    response = receive_message(server_socket)
    file_type = response.decode()
    client_socket_log(f"File type: {file_type}")

    # receive file name
    response = receive_message(server_socket)
    file_name = response.decode()
    client_socket_log(f"File name: {file_name}")

    # receive file content
    response = receive_message(server_socket)
    file_content = response

    save = False
    if file_type == "TRANSACTION_VERIFIED":
        if not os.path.exists(
            os.path.join(constants.processed_transactions_folder, file_name)
        ):
            save = True
        folder = constants.processed_transactions_folder
    elif file_type == "TRANSACTION":
        if not os.path.exists(
            os.path.join(constants.processed_transactions_folder, file_name)
        ):
            save = True
        folder = constants.pending_transactions_folder
    elif file_type == "BLOCK":
        if not os.path.exists(os.path.join(constants.blocks_folder, file_name)):
            save = True
        folder = constants.blocks_folder
    else:
        raise IOError
    file_path = os.path.join(folder, file_name)

    # save file
    if not os.path.exists(file_path) and save:
        with open(file_path, "wb") as f:
            f.write(file_content)
        client_socket_log(f"Saved file to {file_path}")

    return file_type, file_name, file_path

# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 11/10/23

import os
import socket
from typing import Tuple

from src.constants import processed_transactions_folder, blocks_folder

"""
Blockchain socket communication protocol

For syncing transactions and blocks between nodes

Each block/transaction file is sent using the following 3-part message protocol:
1. Send the file type as a message ("TRANSACTION" or "BLOCK")
2. Send the file name as a message (so the client knows what to save it as)
3. Send the file content as a message

Each message is made up of 4 sends/receives on the socket:
1. The server sends the message size (so the client knows how big of a buffer to use)
2. The client confirms that it received the message size
3. The server sends the message content
4. The client confirms that it received the message content

Connection logs are printed and saved to log files.
"""


# Class for connecting nodes and sending transactions and blocks between them.
class NodeConnector:
    log_file_name: str
    processed_transactions_folder: str
    blocks_folder: str

    def __init__(self, node_folder: str):
        self.log_file_name = os.path.join(node_folder, "socket.log")
        self.processed_transactions_folder = os.path.join(
            node_folder, processed_transactions_folder
        )
        self.blocks_folder = os.path.join(node_folder, blocks_folder)

    ### LOG FUNCTIONS

    def log(self, message: str):
        print(message)
        with open(self.log_file_name, "a") as f:
            f.write(message + "\n")

    ### INITIAL CONNECTION FUNCTIONS

    def open_server_socket(self, port: int) -> socket.socket:
        server_address = ("127.0.0.1", port)
        self.log(f"Opening server socket {server_address}")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(server_address)
        server_socket.listen()
        self.log(f"Opened server socket {server_address}")
        return server_socket

    def connect_to_server_socket(self, port: int) -> socket.socket:
        server_address = ("127.0.0.1", port)
        self.log(f"Connecting to server {server_address}")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect(server_address)
        self.log(f"Connected to server {server_address}")
        return server_socket

    def connect_to_client_socket(self, server_socket: socket.socket) -> socket.socket:
        # set timeout to keep it from hanging forever:
        # https://stackoverflow.com/questions/7354476/python-socket-object-accept-time-out
        server_socket.settimeout(1)
        self.log(f"Waiting for client connection")
        client_socket, client_address = server_socket.accept()
        self.log(f"Connected to client {client_address}")
        return client_socket

    ### MESSAGE HELPER FUNCTIONS

    def send_message(self, client_socket: socket.socket, message: bytes):
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

    def receive_message(self, server_socket: socket.socket) -> bytes:
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
        self,
        client_socket: socket.socket,
        file_type: str,
        file_name: str,
        file_path: str,
    ):
        # send file type
        self.send_message(client_socket, file_type.encode())

        # send file name
        self.send_message(client_socket, file_name.encode())

        # read file content
        with open(file_path, "rb") as f:
            content = f.read()

        # send file content
        self.send_message(client_socket, content)

    def send_transaction_file(
        self,
        client_socket: socket.socket,
        file_name: str,
        file_path: str,
    ):
        self.log(f"Sending TRANSACTION file {file_name} to client from {file_path}")
        self.send_file(client_socket, "TRANSACTION", file_name, file_path)
        self.log(f"Sent TRANSACTION file {file_name} to client from {file_path}")
        self.log("---")

    def send_block_file(
        self,
        client_socket: socket.socket,
        file_name: str,
        file_path: str,
    ):
        self.log(f"Sending BLOCK file {file_name} to client from {file_path}")
        self.send_file(client_socket, "BLOCK", file_name, file_path)
        self.log(f"Sent BLOCK file {file_name} to client from {file_path}")
        self.log("---")

    def receive_file(self, server_socket: socket.socket) -> Tuple[str, str, bytes]:
        """
        Receives a transaction or block file from the server socket
        and returns the file type, name, and content.
        """
        self.log("Receiving file")

        # receive file type
        response = self.receive_message(server_socket)
        file_type = response.decode()
        self.log(f"File type: {file_type}")

        # receive file name
        response = self.receive_message(server_socket)
        file_name = response.decode()
        self.log(f"File name: {file_name}")

        # receive file content
        response = self.receive_message(server_socket)
        file_content = response

        return file_type, file_name, file_content

    def save_file(self, file_type, file_name, file_content) -> str:
        """
        Saves a transaction or block file and returns
        the file name without the .json suffix.
        """
        if file_type == "TRANSACTION":
            folder = self.processed_transactions_folder
        elif file_type == "BLOCK":
            folder = self.blocks_folder
        else:
            raise IOError

        file_path = os.path.join(folder, file_name)

        # save file
        with open(file_path, "wb") as f:
            f.write(file_content)
        self.log(f"Saved file to {file_path}")
        self.log("---")

        return file_name.removesuffix(".json")

    def receive_and_save_file(self, server_socket: socket.socket) -> str:
        """
        Receives and saves a transaction or block file from the server socket
        and returns the file name without the .json suffix.
        """
        file_type, file_name, file_content = self.receive_file(server_socket)
        return self.save_file(file_type, file_name, file_content)

import os

from socket_functions import connect_to_server_socket, receive_file
from constants import blocks_folder, processed_transactions_folder

"""
This is a test of socket_functions.py, which sends/receives a block file and a transaction file.

To test:
1. Open side-by-side terminals from the src/ folder
2. Run test_socket_server.py in one terminal
3. Run test_socket_client.py in the other terminal
4. See the files saved in blocks/ and processed/
"""

os.makedirs(blocks_folder, exist_ok=True)
os.makedirs(processed_transactions_folder, exist_ok=True)

server_socket = connect_to_server_socket()
receive_file(server_socket)
receive_file(server_socket)
server_socket.close()

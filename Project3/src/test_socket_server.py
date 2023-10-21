from socket_functions import (
    open_server_socket,
    connect_to_client_socket,
    send_block_file,
    send_transaction_file,
)

"""
This is a test of socket_functions.py, which sends/receives a block file and a transaction file.

To test:
1. Open side-by-side terminals from the src/ folder
2. Run test_socket_server.py in one terminal
3. Run test_socket_client.py in the other terminal
4. See the files saved in blocks/ and processed/
"""

server_socket = open_server_socket()
client_socket = connect_to_client_socket(server_socket)
send_block_file(
    client_socket,
    "test_file_block.txt",
    "./test_file_block.txt",
)
send_transaction_file(
    client_socket,
    "test_file_transaction.txt",
    "./test_file_transaction.txt",
)

# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 11/10/23

import os

from src.connector import NodeConnector

"""
This is a test of connector.py, which sends/receives a block file and a transaction file.

To test:
1. Open side-by-side terminals from the Project4 folder
2. Run python3 -m src.test_connector_server in one terminal
3. Run python3 -m src.test_connector_client in the other terminal
4. See the files saved in the test folder
"""

connector = NodeConnector("test")
server_socket = connector.open_server_socket(5555)
client_socket = connector.connect_to_client_socket(server_socket)
connector.send_block_file(
    client_socket,
    "test_file_block.txt",
    os.path.join("src", "test_file_block.txt"),
)
connector.send_transaction_file(
    client_socket,
    "test_file_transaction.txt",
    os.path.join("src", "test_file_transaction.txt"),
)

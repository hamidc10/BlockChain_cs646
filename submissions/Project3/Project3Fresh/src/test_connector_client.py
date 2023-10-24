# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 10/22/23

import os

from src.connector import NodeConnector
from src.constants import blocks_folder, processed_transactions_folder

"""
This is a test of connector.py, which sends/receives a block file and a transaction file.

To test:
1. Open side-by-side terminals from the Project3 folder
2. Run python3 -m src.test_connector_server in one terminal
3. Run python3 -m src.test_connector_client in the other terminal
4. See the files saved in the test folder
"""

os.makedirs(os.path.join("test", blocks_folder), exist_ok=True)
os.makedirs(os.path.join("test", processed_transactions_folder), exist_ok=True)

connector = NodeConnector("test")
server_socket = connector.connect_to_server_socket(5555)
connector.receive_file(server_socket)
connector.receive_file(server_socket)
server_socket.close()

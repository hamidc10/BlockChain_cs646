from socket_functions import (
    open_server_socket,
    connect_to_client_socket,
    connect_to_peer,
    send_transaction_file,
    receive_file,
)
import os
from random import randrange
from constants import pending_transactions_folder
"""
This is a test of socket_functions.py, which sends/receives a block file and a transaction file.

To test:
1. Open side-by-side terminals from the src/ folder
2. Run test_socket_server.py in one terminal
3. Run test_socket_client.py in the other terminal
4. See the files saved in blocks/ and processed/
"""
# 8000
miners = [("127.0.0.1", 5556), ("127.0.0.1", 5557), ("127.0.0.1", 5558)]

server_socket = open_server_socket()
pending=[]
verified=[]
while True:
    client_socket = connect_to_client_socket(server_socket)
    file_type, file_name, file_path = receive_file(client_socket)

    if file_type == "TRANSACTION" and file_name not in pending:
        print("\nTSX")
        pending.append(file_name)
        miner=miners[randrange(0,3)]
        p2p=connect_to_peer(miner)
        send_transaction_file(p2p,file_name,file_path)
        p2p.close()
    elif file_type == "TRANSACTION_VERIFIED":
        from_pending = os.path.join(pending_transactions_folder, file_name)
        if(os.path.isfile(from_pending)):
            os.remove(from_pending)
            

        
        
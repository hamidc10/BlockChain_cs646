from socket_functions import (
    open_server_socket,
    connect_to_client_socket,
    connect_to_peer,
    send_block_file,
    send_verified_transaction_file,
    receive_file,
)
from miner import verify
from block import Block
import os
import shutil
from constants import processed_transactions_folder, pending_transactions_folder, blocks_folder
"""
This is a test of socket_functions.py, which sends/receives a block file and a transaction file.

To test:
1. Open side-by-side terminals from the src/ folder
2. Run test_socket_server.py in one terminal
3. Run test_socket_client.py in the other terminal
4. See the files saved in blocks/ and processed/
"""
# 8002
# peers = [("127.0.0.1", 5557),("127.0.0.1", 5555)]
peers = [("127.0.0.1",5557),("127.0.0.1",5558)]
server_socket = open_server_socket()

sent_verified_tsxs = []
sent_blocks=[]
verified_tsxs=[]
mined_blocks=Block()

while True:
    client_socket = connect_to_client_socket(server_socket)
    file_type, file_name, file_path = receive_file(client_socket)

    if file_type == "TRANSACTION" and file_name not in verified_tsxs and not os.path.exists(os.path.join(processed_transactions_folder, file_name)):
        print("\nTSX\n")
        good = verify.miner_verify(file_path)
        if good:
            verified_tsxs.append(file_name)
            src_path = os.path.join(pending_transactions_folder, file_name)
            dst_path = os.path.join(processed_transactions_folder, file_name)
            shutil.move(src_path, dst_path)
            print(src_path,dst_path,file_name)
            for peer in peers:
                print(peer)
                p2p = connect_to_peer(peer)
                send_verified_transaction_file(
                    p2p,
                    file_name,
                    dst_path,
                )
                print(dst_path)
                p2p.close()
            sent_verified_tsxs.append(file_name)

    if file_type=="TRANSACTION_VERIFIED" and file_name not in sent_verified_tsxs:
        print("\nTSX_VER\n")
        if file_name not in verified_tsxs:
            verified_tsxs.append(file_name)
        sent_verified_tsxs.append(file_name)
        for peer in peers:
            print(peer)
            p2p = connect_to_peer(peer)
            send_verified_transaction_file(
                p2p,
                file_name,
                file_path,
            )
            print(file_path)
            p2p.close()
    elif file_name in verified_tsxs:
        print(f"{file_name} is already validated")

    if len(verified_tsxs)==1:
        print("\nBLOCK MINED\n")
        block_name=mined_blocks.block_maker(verified_tsxs) 
        for peer in peers:
            print(peer)
            p2p = connect_to_peer(peer)
            send_block_file(
                p2p,
                block_name,
                f'{blocks_folder}/{block_name}',
            )
            p2p.close()
        sent_blocks.append(block_name)
        verified_tsxs=[]

    if file_type=="BLOCK" and file_name not in sent_blocks:
        print("\nBLOCK PROPAGATED\n")
        for peer in peers:
            print(peer)
            p2p = connect_to_peer(peer)
            send_block_file(
                p2p,
                file_name,
                file_path,
            )
            p2p.close()
        sent_blocks.append(file_name)
# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 10/22/23

import os
import time
import datetime
import socket
import json
import hashlib
import shutil

from typing import List

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from src.account_state import (
    init_account_state,
    load_account_state,
    save_account_state,
)
from src.connector import NodeConnector
from src.constants import (
    pending_transactions_folder,
    processed_transactions_folder,
    blocks_folder,
)


class Node:
    pending_transactions_folder: str
    processed_transactions_folder: str
    blocks_folder: str
    connector: NodeConnector
    node_socket: socket.socket
    other_node_socket_ports: List[int]
    file_hash_list: List[str]
    block_hash_list: List[str]

    def __init__(
        self,
        folder: str,
        socket_port: int,
        other_node_socket_ports: List[int],
    ):
        self.pending_transactions_folder = os.path.join(
            folder, pending_transactions_folder
        )
        self.processed_transactions_folder = os.path.join(
            folder, processed_transactions_folder
        )
        self.blocks_folder = os.path.join(folder, blocks_folder)
        os.makedirs(self.pending_transactions_folder, exist_ok=True)
        os.makedirs(self.processed_transactions_folder, exist_ok=True)
        os.makedirs(self.blocks_folder, exist_ok=True)

        self.connector = NodeConnector(folder)
        self.node_socket = self.connector.open_server_socket(socket_port)
        self.other_node_socket_ports = other_node_socket_ports

        self.file_hash_list = []
        self.block_hash_list = []

        init_account_state()

    def new_block(self, transaction_hash: str) -> str | None:
        """
        Receives the file_name that is to be added to the block.
        Once the data is received it then gets put into a dictionary called 'block' as a value to the 'body' key.
        The block is then converted to JSON.
        Returns the block name, or None if the transaction is invalid.
        """

        self.file_hash_list.append(transaction_hash)

        current_time = datetime.datetime.now()
        timestamp = int(datetime.datetime.timestamp(current_time))
        body_list = []

        # Reference used to learn how to read json file content as a dictionary:
        # https://www.geeksforgeeks.org/how-to-read-dictionary-from-file-in-python/

        # Creating the body for the block based on the current transaction.
        with open(
            os.path.join(self.pending_transactions_folder, transaction_hash + ".json"),
            "r",
        ) as f:
            body_dict = {"hash": transaction_hash, "content": json.loads(f.read())}
            body_list.append(body_dict)

        # Validate transaction signature
        # https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html
        transaction = body_dict["content"]
        with open(transaction["PublicKeyFilePath"], "rb") as f:
            public_key_bytes = f.read()
        # We assume that this is the message of the signature:
        # This is the same as the binary value of the sender address:
        public_key_hash = SHA256.new(public_key_bytes)
        # Importing the public key to an RSA object used for validation:
        public_key = RSA.import_key(public_key_bytes)
        # Have to convert signature back from hexadecimal:
        signature = bytes.fromhex(transaction["Signature"])
        try:
            pkcs1_15.new(public_key).verify(public_key_hash, signature)
            print("The transaction signature is valid!")
        except (ValueError, TypeError):
            print("The transaction signature is not valid!")
            return None

        height = self.file_hash_list.index(transaction_hash)
        if height == 0:
            previousblock_hash = "NA"
        else:
            previousblock_hash = self.block_hash_list[height - 1]

            # Appending body of previous block to body of current block.
            with open(
                os.path.join(self.blocks_folder, previousblock_hash + ".json"), "r"
            ) as b:
                body = json.loads(b.read())
                body_list.append(body["body"][0])

        body_str = str(body_list)
        body_str = body_str.replace(" ", "")
        body_hash = hashlib.sha256(body_str.encode("utf-8")).hexdigest()

        # Creating header based on project specifications.
        header_dict = {
            "height": height,
            "timestamp": timestamp,
            "previousblock": previousblock_hash,
            "hash": body_hash,
        }

        header_str = str(header_dict)
        header_str = header_str.replace(" ", "")

        # The file name for the block is the hash of the header.
        block_name = hashlib.sha256(header_str.encode("utf-8")).hexdigest()

        block = {"header": header_dict, "body": body_list}

        with open(
            os.path.join(self.blocks_folder, block_name + ".json"), "w"
        ) as new_block:
            json.dump(block, new_block, indent=None)

        self.block_hash_list.append(block_name)

        # Moving the processed transaction file into the processed folder and deleting the file from the pending folder.
        # https://www.geeksforgeeks.org/how-to-move-all-files-from-one-directory-to-another-using-python/
        src_path = os.path.join(
            self.pending_transactions_folder, transaction_hash + ".json"
        )
        dst_path = os.path.join(
            self.processed_transactions_folder, transaction_hash + ".json"
        )
        shutil.move(src_path, dst_path)

        # Update account state file with new balances
        amount = transaction["Amount"]
        from_address = transaction["From"]
        to_address = transaction["To"]
        account_state = load_account_state()
        account_state[from_address] = account_state.get(from_address, 0) - amount
        account_state[to_address] = account_state.get(to_address, 0) + amount
        save_account_state(account_state)

        print("New Block:\n", json.dumps(block, indent=2))

        return block_name

    def process_pending_transactions(self):
        print("Processing pending transactions")
        if os.path.exists(self.pending_transactions_folder):
            pending_transaction_files = os.listdir(self.pending_transactions_folder)
            if not pending_transaction_files:
                print("No pending transactions found")
            else:
                for transaction_file_name in pending_transaction_files:
                    transaction_hash = transaction_file_name.removesuffix(".json")
                    block_name = self.new_block(transaction_hash)
                    if block_name:
                        block_file_name = block_name + ".json"
                        block_file_path = os.path.join(
                            self.blocks_folder, block_file_name
                        )
                        transaction_file_path = os.path.join(
                            self.processed_transactions_folder, transaction_file_name
                        )
                        for port in self.other_node_socket_ports:
                            other_node_socket = self.connector.connect_to_server_socket(
                                port
                            )
                            self.connector.send_transaction_file(
                                other_node_socket,
                                transaction_file_name,
                                transaction_file_path,
                            )
                            self.connector.send_block_file(
                                other_node_socket,
                                block_file_name,
                                block_file_path,
                            )

    def receive_processed_transaction_and_block(self):
        print("Checking for transactions/blocks from other nodes")
        try:
            other_node_socket = self.connector.connect_to_client_socket(
                self.node_socket
            )
            self.connector.receive_file(other_node_socket)  # Transaction
            self.connector.receive_file(other_node_socket)  # Block
            other_node_socket.close()
        except:  # To ignore timeouts when nothing is being sent
            print("Received no new transactions from other nodes")

    def run(self):
        print("\nNode running\n")
        try:
            while True:
                self.process_pending_transactions()
                time.sleep(2)
                self.receive_processed_transaction_and_block()
                time.sleep(2)
                print()
        except KeyboardInterrupt:
            pass

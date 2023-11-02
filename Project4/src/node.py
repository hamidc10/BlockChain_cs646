# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 11/10/23

import os
import time
import datetime
import socket
import json
import hashlib
import shutil

from typing import List, Tuple

import hashlib
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

from src.account_state import update_account_state
from src.wallet import Wallet
from src.connector import NodeConnector
from src.constants import (
    pending_transactions_folder,
    processed_transactions_folder,
    blocks_folder,
    node_state_file_name,
    coinbase_address,
    default_wallet_balance,
)


class Node:
    pending_transactions_folder: str
    processed_transactions_folder: str
    blocks_folder: str
    node_state_file_path: str
    connector: NodeConnector
    node_socket: socket.socket
    other_node_socket_ports: List[int]
    transaction_hash_list: List[str]
    block_hash_list: List[str]
    previous_block: dict
    wallet: Wallet

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
        self.node_state_file_path = os.path.join(folder, node_state_file_name)
        os.makedirs(self.pending_transactions_folder, exist_ok=True)
        os.makedirs(self.processed_transactions_folder, exist_ok=True)
        os.makedirs(self.blocks_folder, exist_ok=True)

        self.connector = NodeConnector(folder)
        self.node_socket = self.connector.open_server_socket(socket_port)
        self.other_node_socket_ports = other_node_socket_ports

        # Set self.transaction_hash_list and self.block_hash_list
        self.load_node_state()

        self.wait_for_other_nodes_to_start()
        self.wallet = Wallet(folder)  # For creating coinbase
        if not os.listdir(self.blocks_folder):  # Blocks folder empty
            # Create coinbase
            print("Creating coinbase")
            self.wallet.create_coinbase(self.pending_transactions_folder)
        else:
            print("Coinbase already created")

    def load_node_state(self):
        if os.path.exists(self.node_state_file_path):
            with open(self.node_state_file_path, "r") as f:
                node_state = json.load(f)
            self.transaction_hash_list = node_state.get("transaction_hash_list", [])
            self.block_hash_list = node_state.get("block_hash_list", [])
            self.previous_block = node_state.get("previous_block", {})
        else:
            self.transaction_hash_list = []
            self.block_hash_list = []
            self.previous_block = {}

    def save_node_state(self):
        with open(self.node_state_file_path, "w+") as f:
            node_state = {
                "transaction_hash_list": self.transaction_hash_list,
                "block_hash_list": self.block_hash_list,
                "previous_block": self.previous_block,
            }
            json.dump(node_state, f)

    def wait_for_other_nodes_to_start(self):
        print("Waiting for other nodes to start")
        other_nodes_are_ready = False
        while not other_nodes_are_ready:
            other_nodes_are_ready = True
            for port in self.other_node_socket_ports:
                try:
                    self.connector.connect_to_server_socket(port)
                except:
                    other_nodes_are_ready = False
                time.sleep(1)
        print("Other nodes are ready")

    def validate_transaction(self, transaction: dict) -> bool:
        # Prevent negative transactions
        if transaction["Amount"] < 0:
            print("Invalid transaction (amount cannot be negative); REJECTED")
            return False

        # Validate coinbase transactions
        if transaction["From"] == coinbase_address:
            if os.listdir(self.blocks_folder):  # Blocks folder not empty
                print("Invalid coinbase (must be first): REJECTED")
                return False
            if transaction["Amount"] != default_wallet_balance:
                print("Invalid coinbase (unexpected amount): REJECTED")
                return False

        # Validate sender balance (does not apply to coinbase)
        else:
            sender_balance = self.wallet.check_balance(transaction["From"])
            if transaction["Amount"] > sender_balance:
                print("Invalid transaction (sender does not have enough); REJECTED")
                return False

        # Validate transaction signature
        # https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html
        with open(transaction["PublicKeyFilePath"], "rb") as f:
            public_key_bytes = f.read()
        # We assume that this is the message of the signature:
        # This is the same as the binary value of the sender address:
        public_key_hash = hashlib.sha256(public_key_bytes)
        # Importing the public key to an RSA object used for validation:
        public_key = serialization.load_pem_public_key(public_key_bytes)
        # Have to convert signature back from hexadecimal:
        signature = bytes.fromhex(transaction["Signature"])
        try:
            public_key.verify(
                signature,
                public_key_hash.digest(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            print("The transaction signature is valid: ACCEPTED")
        except (ValueError, TypeError):
            print("The transaction signature is not valid: REJECTED")
            return False  # Invalid transactions should not be shared with other nodes

        return True  # Valid

    def new_block(self, transaction_hash: str) -> str | None:
        """
        Receives the file_name that is to be added to the block.
        Once the data is received it then gets put into a dictionary called 'block' as a value to the 'body' key.
        The block is then converted to JSON.
        Returns the block name, or None if the transaction is a coinbase or invalid
        (coinbase/invalid transactions should not be shared with other nodes).
        """

        # TODO: call solve_puzzle (Chantel)
        # read PLAN.md for details

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

        # Validate transaction
        transaction = body_dict["content"]
        if not self.validate_transaction(transaction):
            return None

        self.transaction_hash_list.append(transaction_hash)
        height = self.transaction_hash_list.index(transaction_hash)
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
        self.previous_block = block

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
        update_account_state(transaction)

        # Save updated node state
        self.save_node_state()

        print("New Block:\n", json.dumps(block, indent=2))

        if transaction["From"] == coinbase_address:
            return None  # Coinbases should not be shared with other nodes
        return block_name

    def process_first_pending_transaction(self):
        if os.path.exists(self.pending_transactions_folder):
            pending_transaction_files = sorted(
                os.listdir(self.pending_transactions_folder)
            )
            if not pending_transaction_files:
                print("No pending transaction found")
            else:
                print("Processing pending transaction")
                first_pending_transaction = pending_transaction_files[0]
                transaction_hash = first_pending_transaction.removesuffix(".json")
                block_name = self.new_block(transaction_hash)
                if block_name:
                    block_file_name = block_name + ".json"
                    block_file_path = os.path.join(self.blocks_folder, block_file_name)
                    for port in self.other_node_socket_ports:
                        other_node_socket = self.connector.connect_to_server_socket(
                            port
                        )
                        self.connector.send_block_file(
                            other_node_socket,
                            block_file_name,
                            block_file_path,
                        )

    def receive_processed_block(self) -> Tuple[str, bytes]:
        """
        Checks for a processed block from another node and returns
        the file name and file content if one is received.
        Returns empty string if no block was received.
        """
        print("Checking for a processed block from another node")
        try:
            other_node_socket = self.connector.connect_to_client_socket(
                self.node_socket
            )
            # Receive block
            file_type, file_name, file_content = self.connector.receive_file(
                other_node_socket
            )
            # Close socket
            other_node_socket.close()
            return file_name, file_content
        except:  # To ignore timeouts when nothing is being sent
            print("Received no new transactions from other nodes")
            return "", b""

    def run(self):
        print("\nNode running\n")
        try:
            while True:
                self.process_first_pending_transaction()
                time.sleep(1)
                print()
        except KeyboardInterrupt:
            pass

    def solve_puzzle(self):
        # TODO: implement this (Chantel)
        # read PLAN.md for details
        pass

    def check_for_competing_blocks(self):
        # TODO: implement this (Hamid)
        # read PLAN.md for details
        pass

    def accept_winning_block(self):
        # TODO: implement this (Hamid)
        # read PLAN.md for details
        pass

    def validate_block(self):
        # TODO: implement this (Trey)
        # read PLAN.md for details
        pass

    def pick_winning_block(self, header, transactions, height):
        # TODO: implement this (Xavier)
        # read PLAN.md for details
        
        #given a list of block objects
       self.Blockheader = header
       self.Blocktransactions = transactions
       self.Blockheight = height

       block_list=[]
       block_list.append(Node(header, transactions, height))
        #return the block that has the smallest "Nonce" value in its header

        pass

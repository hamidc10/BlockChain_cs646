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
from uuid import uuid4
from typing import List, Dict, Tuple

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

from src.account_state import update_account_state
from src.wallet import Wallet
from src.connector import NodeConnector
from src.constants import (
    pending_transactions_folder,
    processed_transactions_folder,
    rejected_transactions_folder,
    blocks_folder,
    node_state_file_name,
    coinbase_address,
    default_wallet_balance,
)


class Node:
    pending_transactions_folder: str
    processed_transactions_folder: str
    rejected_transactions_folder: str
    blocks_folder: str
    node_state_file_path: str
    connector: NodeConnector
    node_socket: socket.socket
    other_node_socket_ports: List[int]
    transaction_hash_list: List[str]
    block_hash_list: List[str]
    previous_block: Dict
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
        self.rejected_transactions_folder = os.path.join(
            folder, rejected_transactions_folder
        )
        self.blocks_folder = os.path.join(folder, blocks_folder)
        self.node_state_file_path = os.path.join(folder, node_state_file_name)
        os.makedirs(self.pending_transactions_folder, exist_ok=True)
        os.makedirs(self.processed_transactions_folder, exist_ok=True)
        os.makedirs(self.rejected_transactions_folder, exist_ok=True)
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
                except (ConnectionRefusedError, TimeoutError):
                    other_nodes_are_ready = False
                time.sleep(1)
        print("Other nodes are ready")

    def validate_transaction_signature(self, transaction: Dict) -> bool:
        # Validate transaction signature
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

    def validate_transaction(self, transaction: Dict) -> bool:
        """
        Validates a transaction to be processed.
        """
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
        return self.validate_transaction_signature(transaction)

    def validate_processed_transaction(self, transaction: Dict) -> bool:
        """
        Validates a transaction already processed by another node.
        """
        # Prevent negative transactions
        if transaction["Amount"] < 0:
            print("Invalid transaction (amount cannot be negative); REJECTED")
            return False

        # Validate transaction signature
        return self.validate_transaction_signature(transaction)

    def get_object_hash(self, obj: List | Dict) -> str:
        s = json.dumps(obj, sort_keys=True)
        return hashlib.sha256(s.encode()).hexdigest()

    def get_block_name(self, block: Dict) -> str:
        """
        Returns the block header hash to be used as the block name.
        """
        return self.get_object_hash(block["header"])

    def save_block(self, block: Dict) -> str:
        """
        Saves the given block as a JSON file in the blocks folder, sets it as the previous block,
        adds it's header hash to the block hash list, and returns the block header hash.
        """
        block_name = self.get_block_name(block)
        with open(os.path.join(self.blocks_folder, block_name + ".json"), "w") as f:
            json.dump(block, f, sort_keys=True)
        self.block_hash_list.append(block_name)
        self.previous_block = block
        return block_name

    def move_processed_transaction(self, block: Dict):
        """
        Moves the transaction associated with the given block
        from the pending folder to the processed folder.
        """
        transaction_hash = block["body"][0]["hash"]
        # Moving the processed transaction file into the processed folder and deleting the file from the pending folder.
        # https://www.geeksforgeeks.org/how-to-move-all-files-from-one-directory-to-another-using-python/
        src_path = os.path.join(
            self.pending_transactions_folder, transaction_hash + ".json"
        )
        dst_path = os.path.join(
            self.processed_transactions_folder, transaction_hash + ".json"
        )
        shutil.move(src_path, dst_path)

    def move_rejected_transaction(self, transaction_hash: str):
        """
        Moves the given transaction from the pending folder to the rejected folder.
        """
        src_path = os.path.join(
            self.pending_transactions_folder, transaction_hash + ".json"
        )
        dst_path = os.path.join(
            self.rejected_transactions_folder, transaction_hash + ".json"
        )
        shutil.move(src_path, dst_path)

    def new_block(self, transaction_hash: str) -> str | None:
        """
        Receives the file_name that is to be added to the block.
        Once the data is received it then gets put into a dictionary called 'block' as a value to the 'body' key.
        The block is then converted to JSON.
        Returns the block name, or None if the transaction is a coinbase or invalid
        (coinbase/invalid transactions should not be shared with other nodes).
        """

        # Read transaction file
        with open(
            os.path.join(self.pending_transactions_folder, transaction_hash + ".json"),
            "r",
        ) as f:
            transaction = json.load(f)

        # Validate transaction
        if not self.validate_transaction(transaction):
            self.move_rejected_transaction(transaction_hash)
            return None

        # Attempt to solve puzzle in order to mine block
        solved_puzzle, winning_nonce = self.solve_puzzle()
        if not solved_puzzle:
            return None

        # Starting mining block
        current_time = datetime.datetime.now()
        timestamp = int(datetime.datetime.timestamp(current_time))
        body_list = []

        # Reference used to learn how to read json file content as a dictionary:
        # https://www.geeksforgeeks.org/how-to-read-dictionary-from-file-in-python/

        # Creating the body for the block based on the current transaction.
        body_dict = {"hash": transaction_hash, "content": transaction}
        body_list.append(body_dict)

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

        # Get body hash
        body_hash = self.get_object_hash(body_list)

        # Creating header based on project specifications.
        header_dict = {
            "height": height,
            "timestamp": timestamp,
            "previousblock": previousblock_hash,
            "hash": body_hash,
            "nonce" : winning_nonce
        }

        # Create block object
        block = {"header": header_dict, "body": body_list}

        # Save block file
        block_name = self.save_block(block)

        # Mark transaction as processed
        self.move_processed_transaction(block)

        # Update account state file with new balances
        update_account_state(transaction)

        # Save updated node state
        self.save_node_state()

        print("New Block:\n", json.dumps(block, indent=2, sort_keys=True))

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

    def receive_processed_block(self) -> Dict | None:
        """
        Checks for a processed block from another node and returns one if received.
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
            return json.loads(file_content)
        except (ConnectionResetError, TimeoutError, ValueError):
            # To ignore timeouts when nothing is being sent
            print("Received no new transactions from other nodes")
            return None

    def solve_puzzle(self) -> Tuple[bool, int]:
        """
        Attempts to solve the puzzle to mine the next block,
        following the algorithm shown in the TA corner video.
        Returns True and the winning nonce value if this node solved the puzzle first.
        Returns False if the another node solved the puzzle first, and handles
        acceptance of the winning block from the other node in this case as well.
        """
        # Add empty header object for coinbase case
        if not self.previous_block.get("header"):
            self.previous_block["header"] = {}

        # Prevent all nodes from generating the same hashes
        self.previous_block["Random"] = uuid4().hex

        nonce = 0
        target = "0"
        while True:
            competing_blocks = self.check_for_competing_blocks()
            if competing_blocks:
                print("Lost puzzle challenge; accepting block from winning node...")
                winning_block = self.pick_winning_block(competing_blocks)
                self.accept_winning_block(winning_block)
                return False, 0
            self.previous_block["header"]["nonce"] = nonce
            json_value = json.dumps(self.previous_block, sort_keys=True)
            block_hash = hashlib.sha256(json_value.encode()).hexdigest()
            print(f"Attempting puzzle: nonce={nonce} hash={block_hash}")
            if block_hash[0 : len(target)] == target:
                print("Won puzzle challenge; mining block...")
                return True, nonce
            nonce += 1

    def check_for_competing_blocks(self) -> List[Dict]:
        """
        Returns a list of competing blocks mined by other nodes.
        """
        print("Checking for competing blocks mined by other nodes...")
        competing_blocks = []
        block = self.receive_processed_block()
        if block and self.validate_block(block):
            competing_blocks.append(block)
        return competing_blocks

    def accept_winning_block(self, block: Dict):
        """
        Saves the given block, marks the associated transaction as processed,
        and updates the node's state.
        """
        self.save_block(block)
        self.move_processed_transaction(block)
        self.save_node_state()


    def validate_block(self, block: Dict) -> bool:
        """
        Validates the block using the checks listed in Canvas.
        -- Nodes validate all the transaction in the block
        -- Nodes validate that the calculated hash root matches what is included in the header
        -- Nodes validate that the block height is 1 block higher than the previous block
        -- Nodes validate that the previous block hash matches a block (that was previously validated) that has the current height - 1
        """
        print("Validating block from other node...")

        for transaction in block["body"]:
            if not self.validate_processed_transaction(transaction["content"]):
                print("Invalid block transaction; REJECTED")
                return False

        if block["header"]["hash"] != self.get_object_hash(block["body"]):
            print("Invalid block hash; REJECTED")
            return False

        if block["header"]["height"] != (self.previous_block["header"]["height"] + 1):
            print("Invalid block height; REJECTED")
            return False

        # Note: blocks with height=1 have previous blocks as coinbase of other node and hashes will not match
        if block["header"]["height"] > 1 and block["header"]["previousblock"] != self.block_hash_list[-1]:
            print("Invalid previous block; REJECTED")
            return False

        print("Block is valid; ACCEPTED")
        return True

    def pick_winning_block(self, blocks: List[Dict]) -> Dict:
        """
        Returns the block with the smallest nonce value.
        """
        smallest_nonce = -1
        winning_block = {}
        for block in blocks:
            nonce = block["header"]["nonce"]
            if smallest_nonce == -1:
                smallest_nonce = nonce
                winning_block = block
            elif nonce < smallest_nonce:
                smallest_nonce = nonce
                winning_block = block
        return winning_block

    def run(self):
        print("\nNode running\n")
        try:
            while True:
                self.process_first_pending_transaction()
                time.sleep(2)
                print()
        except KeyboardInterrupt:
            pass

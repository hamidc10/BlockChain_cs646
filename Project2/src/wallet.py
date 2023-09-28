# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 10/1/23

import os

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

from transaction import new_transaction
from account_state import load_account_state
from constants import keys_folder


class Wallet:
    name: str
    address: str
    signature: bytes
    public_key_file_path: str
    private_key_file_path: str

    def __init__(self, name: str):
        """
        Initializes the wallet by loading/creating keys,
        setting the address, and creating a signature.
        """
        self.name = name

        public_key_file_name = name.replace(" ", "") + "_key.pub"
        self.public_key_file_path = os.path.join(keys_folder, public_key_file_name)

        private_key_file_name = name.replace(" ", "") + "_key"
        self.private_key_file_path = os.path.join(keys_folder, private_key_file_name)

        # check if the user's RSA key files (public and private) exist
        public_key_exists = os.path.exists(self.public_key_file_path)
        private_key_exists = os.path.exists(self.private_key_file_path)
        if public_key_exists and private_key_exists:
            # if the keys exist, load them
            with open(self.public_key_file_path, "rb") as f:
                public_key_bytes = f.read()
            with open(self.private_key_file_path, "rb") as f:
                private_key_bytes = f.read()
        else:
            # if the keys don't exist, create/save a new RSA public/private key pair for the user
            # https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html
            private_key = RSA.generate(2048)
            private_key_bytes = private_key.export_key()
            public_key_bytes = private_key.publickey().export_key()
            with open(self.private_key_file_path, "wb") as f:
                f.write(private_key_bytes)
            with open(self.public_key_file_path, "wb") as f:
                f.write(public_key_bytes)

        # set user address to be the SHA256 hash of the user's public key
        # https://pycryptodome.readthedocs.io/en/latest/src/hash/sha256.html
        public_key_hash = SHA256.new(public_key_bytes)
        public_key_hash_str = public_key_hash.hexdigest()
        self.address = public_key_hash_str

        # set user signature to be the user address signed by the user's private key
        # https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html
        private_key = RSA.import_key(private_key_bytes)
        self.signature = pkcs1_15.new(private_key).sign(public_key_hash)

    def send(self, to_address: str, amount: int) -> str:
        """
        Sends the specified amount to the user with the specified address through
        a transaction on the blockchain and returns the hash of the transaction.
        """
        return new_transaction(
            self.address,
            to_address,
            amount,
            self.signature,
            self.public_key_file_path,
        )

    def check_balance(self, address: str = "") -> int:
        """
        Returns the account balance of the user with the given address
        (or the user of this wallet if no address is given)
        from the account state file.
        """
        if address == "":
            address = self.address
        # load account state file (JSON) into a dictionary
        account_dict = load_account_state()
        # return the value in the account state dictionary under the given address
        return account_dict.get(address, 0)

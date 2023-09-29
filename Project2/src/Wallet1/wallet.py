# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 10/1/23

import os
import rsa
from transaction import new_transaction
from constants import keys_folder
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import hashlib
import json


class Wallet:
    name: str
    count: int
    address: str
    signature: bytes

    def __init__(self, name: str):
        """
        Initializes the wallet by loading/creating keys,
        setting the address, and creating a signature.
        """
        self.name = name

        f = open(f"{self.name}/private.pem", "rb")
        pk = serialization.load_pem_private_key(f.read(), password=None)
        pbk = pk.public_key()
        pem = pbk.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        # reference used to remove unicode error https://stackoverflow.com/questions/42339876/error-unicodedecodeerror-utf-8-codec-cant-decode-byte-0xff-in-position-0-in
        pem_bytes = pem[27:-25]
        self.address = hashlib.sha256(pem_bytes).hexdigest()
        pem_str = "".join(pem.decode("utf-8").splitlines()[1:-2])
        self.address = hashlib.sha256(pem_str.encode("utf-8")).hexdigest()

    def send(self, to_address: str, amount: int) -> str:
        """
        Sends the specified amount to the user with the specified address through
        a transaction on the blockchain and returns the hash of the transaction.
        """
        # f = open(f"{self.name}/private.pem", "rb")
        with open(f"{self.name}/private.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )
        # pk = serialization.load_pem_private_key(f.read(), password=None)
        data = {
            "From": self.address,
            "To": to_address,
            "Amount": amount,
        }
        message = json.dumps(data).encode("utf-8")
        print(message)
        self.signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        # self.signature=private_key.sign(message)
        print(self.signature)
        return new_transaction(self.address, to_address, amount, str(self.signature))

    def check_balance(self, address: str = "") -> int:
        """
        Returns the account balance of the user with the given address
        (or the user of this wallet if no address is given)
        from the account state file.
        """
        if address == "":
            address = self.address
        # TODO: load account state file (JSON) into a dictionary
        # TODO: return the value in the account state dictionary under the given address
        return 0

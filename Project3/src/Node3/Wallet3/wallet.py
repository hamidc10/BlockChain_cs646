# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 10/1/23

import os
from transaction import new_transaction
from constants import keys_folder
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import hashlib
import json
import account_state


# class Wallet:
#     node: str
#     name: str
#     address: str
#     signature: bytes
    
#     def __init__(self, node, name):
#         self.node = node
#         self.name = name

#         # Debugging: Print the constructed path
#         wallet_directory = os.path.join(node, name)
#         print(f"Constructed wallet directory path: {wallet_directory}")

#         os.makedirs(wallet_directory, exist_ok=True)

#         priv_file = os.path.join(wallet_directory, "private.pem")
#         print(f"Constructed private.pem file path: {priv_file}")

#         if os.path.exists(priv_file):
#             with open(priv_file, "rb") as f:
#                 priv_key = serialization.load_pem_private_key(f.read(), password=None)
#         else:
#             priv_key = rsa.generate_private_key(
#                 public_exponent=65537,
#                 key_size=2048,
#             )
#             pem_priv = priv_key.private_bytes(
#                 encoding=serialization.Encoding.PEM,
#                 format=serialization.PrivateFormat.PKCS8,
#                 encryption_algorithm=serialization.NoEncryption(),
#             )
#             with open(f"{self.name}/private.pem", "wb+") as f:
#                 f.write(pem_priv)


#         pub_key = priv_key.public_key()
#         pem_pub = pub_key.public_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PublicFormat.SubjectPublicKeyInfo,
#         )

#         # reference used to remove unicode error https://stackoverflow.com/questions/42339876/error-unicodedecodeerror-utf-8-codec-cant-decode-byte-0xff-in-position-0-in
#         pem_str = "".join(pem_pub.decode("utf-8").splitlines()[1:-2])
#         self.address = hashlib.sha256(pem_str.encode("utf-8")).hexdigest()
        
#         pub_file = f"{keys_folder}/{self.address}.pem"
#         with open(pub_file, "wb+") as f:
#             f.write(pem_pub)

#     def send(self, to_address: str, amount: int) -> str:
#         """
#         Sends the specified amount to the user with the specified address through
#         a transaction on the blockchain and returns the hash of the transaction.
#         """
        
#         with open(f"{self.name}/private.pem", "rb") as key_file:
#             private_key = serialization.load_pem_private_key(
#                 key_file.read(),
#                 password=None,
#             )
        
#         data = {
#             "From": self.address,
#             "To": to_address,
#             "Amount": amount,
#         }
        
#         message = json.dumps(data).encode("utf-8")
        
#         self.signature = private_key.sign(
#             message,
#             padding.PSS(
#                 mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
#             ),
#             hashes.SHA256(),
#         )

#         return new_transaction(self.address, to_address, amount, self.signature.hex())

#     def check_balance(self, address: str = "") -> int:
#         """
#         Returns the account balance of the user with the given address
#         (or the user of this wallet if no address is given)
#         from the account state file.
#         """
#         if address == "":
#             address = self.address

#         balance_dict = account_state.load_account_state()

#         try:
#             return balance_dict[address]
#         except:
#             return 0

class Wallet:
    node: str
    name: str
    address: str
    signature: bytes
    def __init__(self, node, name):
        self.node = node
        self.name = name

        # Construct the path to the private key file
        wallet_directory = os.path.join(node, name)  # The wallet directory inside the node
        os.makedirs(wallet_directory, exist_ok=True)  # Create the wallet directory if it doesn't exist

        priv_file = os.path.join(wallet_directory, "private.pem")  # Path to private key
        if os.path.exists(priv_file):
            with open(priv_file, "rb") as f:
                priv_key = serialization.load_pem_private_key(f.read(), password=None)
        else:
            priv_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            pem_priv = priv_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
            with open(priv_file, "wb+") as f:
                f.write(pem_priv)

        pub_key = priv_key.public_key()
        pem_pub = pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        # Reference used to remove a Unicode error: https://stackoverflow.com/questions/42339876/error-unicodedecodeerror-utf-8-codec-cant-decode-byte-0xff-in-position-0-in
        pem_str = "".join(pem_pub.decode("utf-8").splitlines()[1:-2])
        self.address = hashlib.sha256(pem_str.encode("utf-8")).hexdigest()

        pub_file = os.path.join(wallet_directory, "public.pem")  # Path to public key
        with open(pub_file, "wb+") as f:
            f.write(pem_pub)

    def send(self, to_address: str, amount: int) -> str:
        """
        Sends the specified amount to the user with the specified address through
        a transaction on the blockchain and returns the hash of the transaction.
        """

        priv_file = os.path.join(self.node, self.name, "private.pem")
        with open(priv_file, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )

        data = {
            "From": self.address,
            "To": to_address,
            "Amount": amount,
        }

        message = json.dumps(data).encode("utf-8")

        self.signature = private_key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )

        return new_transaction(self.address, to_address, amount, self.signature.hex())

    def check_balance(self, address: str = "") -> int:
        """
        Returns the account balance of the user with the given address
        (or the user of this wallet if no address is given)
        from the account state file.
        """
        if address == "":
            address = self.address

        balance_dict = account_state.load_account_state()

        try:
            return balance_dict[address]
        except:
            return 0


# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 10/1/23

import os
import rsa
from transaction import new_transaction
from constants import keys_folder


class Wallet:
    name: str
    count: int
    address: str
    signature: str


    def __init__(self, name: str ):
        """
        Initializes the wallet by loading/creating keys,
        setting the address, and creating a signature.
        """
        self.name = name
        public_key, private_key = rsa.newkeys(1024)
        # wallet_path = "../Project2/wallets/"
        
        # pub_key_pem = "keys/public/"
        # prv_key_pem = "keys/private/"

        # wallet_path_1="wallets/"+name+"_wallet/"+pub_key_pem
        # wallet_path_2="wallets/"+name+"_wallet/"+prv_key_pem
        # os.makedirs(wallet_path_1,exist_ok=True)
        # os.makedirs(wallet_path_2,exist_ok=True)
       
       
        # if not os.path.exists(wallet_path_1+"/pub.pem"):
            
        #     with open(wallet_path_1+"/public.pem", "wb+") as f:
        #         f.write(public_key.save_pkcs1("PEM"))

        #     with open(wallet_path_2+"/private.pem", "wb+") as f:
        #         f.write(private_key.save_pkcs1("PEM"))
            
 
       

        public_key_file_name = name.replace(" ", "") + "_key.pub"
        public_key_file_path = os.path.join(keys_folder, public_key_file_name)

        private_key_file_name = name.replace(" ", "") + "_key"
        public_key_file_path = os.path.join(keys_folder, private_key_file_name)

        # TODO: check if the user's RSA key files (public and private) exist
        # TODO: if the keys exist, load them
        # TODO: if the keys don't exist, create/save a new RSA public/private key pair for the user
        # TODO: set user address to be the SHA256 hash of the user's public key
        self.address = ""
        # TODO: set user signature to be the user address signed by the user's private key
        self.signature = ""

    def send(self, to_address: str, amount: int) -> str:
        """
        Sends the specified amount to the user with the specified address through
        a transaction on the blockchain and returns the hash of the transaction.
        """
        return new_transaction(self.address, to_address, amount, self.signature)

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

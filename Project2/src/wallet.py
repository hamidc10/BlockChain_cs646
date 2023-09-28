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
from cryptography.hazmat.primitives.asymmetric import padding, utils
import hashlib




class Wallet:
    name: str
    count: int
    address: str
    signature: bytes


    def __init__(self, name: str ):
        """
        Initializes the wallet by loading/creating keys,
        setting the address, and creating a signature.
        """
        self.name = name

        
        f= open(f"{self.name}/private.pem","rb") 
        pk=serialization.load_pem_private_key(f.read(),password=None)
        pbk = pk.public_key()
        pem = pbk.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

       
       
        pem_str=''.join(pem.decode('utf-8').splitlines()[1:-2]) 
        print(pem_str)
        self.address = hashlib.sha256(pem_str.encode('utf-8')).hexdigest()
       
    
        # TODO: set user signature to be the user address signed by the user's private key
        # self.signature=pk.sign( "bob",padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
        # print(self.signature)
    def send(self, to_address: str, amount: int) -> str:
        """
        Sends the specified amount to the user with the specified address through
        a transaction on the blockchain and returns the hash of the transaction.
        """
        f= open(f"{self.name}/private.pem","rb") 
        pk=serialization.load_pem_private_key(f.read(),password=None)
        chosen_hash = hashes.SHA256()
        hasher = hashes.Hash(chosen_hash)
        hasher.update(b"data & ")
        hasher.update(b"more data")
        message=self.address.encode("utf-8")+to_address.encode("utf-8")+str(amount).encode("utf-8")
        digest = hasher.finalize()
        self.signature = pk.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print()
        # pem_str=''.join(pk.decode('utf-8').splitlines()[1:-2])

        # self.signature=pk.sign( "transaction",padding.PSS(mgf=padding.MGF1(hashes.SHA256()),salt_length=padding.PSS.MAX_LENGTH),hashes.SHA256())
        
      
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

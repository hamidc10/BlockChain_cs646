# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 10/1/23

import datetime
import json
import hashlib
import os
import shutil
import re
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

from account_state import init_account_state, load_account_state, save_account_state
from constants import (
    pending_transactions_folder,
    processed_transactions_folder,
    blocks_folder,
    keys_folder,
)


class Block:

    """
    TASK for Block file
    Similar to a transaction, a block should be treated as an object that can be stored as a .json file.
    The block should be made up of two main parts, a header and a body.  The body should include a list/array of transactions included in the block.
    The header should include the following:
    Block height(the order the block was created, initial block would be height 0, next block would be height 1, etc..)
    Timestamp
    Hash of the Previous Block (for a block of height 0 you can just use "NA")
    Hash of the Block Body for the current block
    When the file is saved, hash the header content only and use the resulting hash as the name of the file.

    The body is a list of dictionaries of the the current transaction added to the block + the previous transactions.
    """

    def __init__(self, print_block):
        self.file_hash_list = []
        self.block_hash_list = []
        self.print_block = print_block
        init_account_state()

    def new_block(self, transaction_hash: str):
        """
        Receives the file_name that is to be added to the block.
        Once the data is received it then gets put into a dictionary called 'block' as a value to the 'body' key.
        The block is then converted to JSON.
        Used this for help with JSON writing to file:
        https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
        """

        self.file_hash_list.append(transaction_hash)

        current_time = datetime.datetime.now()
        timestamp = int(datetime.datetime.timestamp(current_time))
        body_list = []

        # Reference used to learn how to read json file content as a dictionary:
        # https://www.geeksforgeeks.org/how-to-read-dictionary-from-file-in-python/

        # Creating the body for the block based on the current transaction.
        f = open(pending_transactions_folder + transaction_hash + ".json", "r")
        transaction_dict = json.loads(f.read())
        transaction_body = transaction_dict["transaction"]
        sender_name = transaction_dict["details"]
        public_key_file = f"{keys_folder}/{sender_name}.pem"

        # Validate transaction on blockchain
        pem = open(public_key_file, "rb")
        public_key = serialization.load_pem_public_key(pem.read())

        garbage_message = json.dumps({"j": "jkl"}).encode("utf-8")
        # replace data_to_verify below with garbage message to see what happens if unable to verify
       
        try:
            # https://www.w3schools.com/python/gloss_python_check_if_dictionary_item_exists.asp
            # https://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python
            
            # Checking transaction only has the expected keys: timestamp, from, to, amount, signature
            transaction_keys=transaction_body.keys()
            should_only_have_keys = ["Timestamp", "From", "To", "Amount", "Signature"]
            if not all(keys in transaction_keys for keys in should_only_have_keys):
                print(transaction_keys,"\n",f"dict_keys({should_only_have_keys})")
                print("Transaction format wrong!")
                raise Exception(
                    'Transaction format wrong!'
                )

            data = {
                "From": transaction_body["From"],
                "To": transaction_body["To"],
                "Amount": transaction_body["Amount"],
            }
            
            data_to_verify = json.dumps(data).encode("utf-8")
            signature = bytes.fromhex(transaction_body["Signature"])
            
            public_key.verify(
                signature,
                data_to_verify,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )

            f.close()

            body_dict = {"hash": transaction_hash, "content": transaction_body}
            body_list.append(body_dict)

            height = self.file_hash_list.index(transaction_hash)
            if height == 0:
                previousblock_hash = "NA"
            else:
                previousblock_hash = self.block_hash_list[height - 1]

                #  Appending body of previous block to body of current block.
                with open(blocks_folder + previousblock_hash + ".json", "r") as b:
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

            # os.makedirs(blocks_folder, exist_ok=True)

            with open(blocks_folder + block_name + ".json", "w") as new_block:
                json.dump(block, new_block, indent=None)

            self.block_hash_list.append(block_name)

            # Moving the processed transaction file into the processed folder and deleting the file from the pending folder.
            # https://www.geeksforgeeks.org/how-to-move-all-files-from-one-directory-to-another-using-python/
            src_path = os.path.join(
                pending_transactions_folder, transaction_hash + ".json"
            )
            
            dst_path = os.path.join(
                processed_transactions_folder, transaction_hash + ".json"
            )
            shutil.move(src_path, dst_path)
            
            # TODO: ----------- DELETE THE STEPS BELOW AFTER DONE ------------------------
            
            # get "From", "To", "Amount" from transaction_body and store in seperate variables. 
            # call load_account_state() and assign to a variable. (the variable will store the dictionary that the function returns)
            # at the value of "from_address" in the dictionary store the new balance: account_state.get(from_address,0) - amount
            # check the "to_address" amount if it's <0 then consider the amount as 0 then
            # repeat the above step for the "to_address" and replace "- amount" with "+ amount" 
            # call save_account_state(account_state)
            
            # Made regex to check for capital or lower case y since in NLP and wanted to implement something I learned
            if re.match(r"^[yY]+", self.print_block):
                print("\nNew Block:\n", json.dumps(block, indent=3))
            
        except:
            print("Unable to add transaction to block: Transaction DENIED")

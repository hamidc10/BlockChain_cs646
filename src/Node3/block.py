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

from constants import (
    account_state_file_path,
    pending_transactions_folder,
    processed_transactions_folder,
    blocks_folder,
    keys_folder
)


class Block:
    file_hash_list = []
    block_hash_list = []
    previous_block_hash=""
    def __init__(self):
        self.file_hash_list = []
        self.block_hash_list = []
        
        files = os.listdir(blocks_folder)
        max_height=-1
        for file in files:
            with open(f"{blocks_folder}/{file}","r") as f:
                block= json.loads(f.read())
                height=block["header"]["height"]
                if max_height<height:
                    name_lt=file.split(".")
                    self.previous_block_hash=name_lt[0]
                    max_height=height 
              
        # self.print_block = print_block
        # if not os.path.exists(account_state_file_path):
        #     init_account_state()

    def block_maker(self,file_list):
        current_time = datetime.datetime.now()
        timestamp = int(datetime.datetime.timestamp(current_time))
        body_list = []
   
        for file in file_list:
            f = open(processed_transactions_folder+file, "r")
            transaction_body = json.loads(f.read())     
            path_getter=file.split("/")
            name_list=path_getter[-1].split(".")
            transaction_hash=name_list[0]      
            body_dict = {"hash": transaction_hash, "content": transaction_body}
            body_list.append(body_dict)
            f.close()

        height = len(os.listdir(blocks_folder))
        if height == 0:
            previousblock_hash = "NA"
        else:
            previousblock_hash = self.previous_block_hash

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
        self.block_hash_list.append(block_name)

        with open(blocks_folder + block_name + ".json", "a+") as new_block:
            json.dump(block, new_block, indent=None)
        return f'{block_name}.json'
        

   
        # # updates account balance
        # amount = transaction_body["Amount"]
        # from_address = transaction_body["From"]
        # to_address = transaction_body["To"]
        # account_state = load_account_state()
        # account_state[from_address] = account_state.get(from_address, 0) - amount
        # account_state[to_address] = account_state.get(to_address, 0) + amount
        # save_account_state(account_state)
        
        # Made regex to check for capital or lower case y since in NLP and wanted to implement something I learned
        # if re.match(r"^[yY]+", self.print_block):
        #     print("\nNew Block:\n", json.dumps(block, indent=3))

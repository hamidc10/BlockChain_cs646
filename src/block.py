import datetime
import json
import hashlib
import os
from dataclasses import dataclass


# TASK for Block file
# Similar to a transaction, a block should be treated as an object that can be stored as a .json file. 
# The block should be made up of two main parts, a header and a body.  The body should include a list/array of transactions included in the block.  
# The header should include the following:
# Block height(the order the block was created, initial block would be height 0, next block would be height 1, etc..)
# Timestamp
# Hash of the Previous Block (for a block of height 0 you can just use "NA")
# Hash of the Block Body for the current block 
# When the file is saved, hash the header content only and use the resulting hash as the name of the file. 

# @dataclass
# class Block:
#     header: dict[str:str]
#     body: dict[str:list[dict]]

class Block:
    
    def __init__(self,Height,Timestamp,Previous, Hash):
        self.height=Height
        self.timestamp=Timestamp
        self.previousblock=Previous
        self.hash=Hash

    # This gets the input from the transaction.py file
    # Once the data is received it then get put into a dictionary which would be converted to JSON
    # Used this for help with JSON writing to file:
    #    -https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/

    
    # Before we save the file we need to hash it by using SHA256
    # I took the dictionary and make it into a str with no space then I can hash it using hashlib library
    # After we hash it, The file for the JSON will be saved as hash we created
    # Used this to help me understand how hashlib worked
    #   -https://docs.python.org/3/library/hashlib.html 
    # I had an error with "String must be encoded" found this to help
    #   -https://bobbyhadz.com/blog/python-typeerror-strings-must-be-encoded-before-hashing


    folder_name="/workspaces/BlockChain_cs646/pending/"
    Height=0
    current_time=datetime.datetime.now()
    Timestamp=int(datetime.datetime.timestamp(current_time))
    if(Height==0):
        Previous="NA"
    else: 
        Previous=Previous
        
    body_list=[]

    with open(folder_name+Previous+".json","r") as f:
        body_dict={"hash":Previous,"content":f}
        body_list.append(body_dict)
        print(body_dict)
    #copy the this file into the processed folder and delete the file from pending
    #https://stackoverflow.com/questions/123198/how-to-copy-files
    body={"body":body_list}
    Body_str=str(body)
    Body_str=Body_str.replace(" ","")
    Hash=hashlib.sha256(Body_str.encode('utf-8')).hexdigest()
    
    header_dict={
        "height": Height,
        "timestamp":Timestamp,
        "previousblock":Previous,
        "hash":Hash
    }

    header={"header":header_dict}
    Header_str=str(header)
    Header_str=Header_str.replace(" ","")
    blocks="/workspaces/BlockChain_cs646/blocks/"
    file_name=hashlib.sha256(Header_str.encode('utf-8')).hexdigest()
    
    with open(blocks+file_name+".json","w") as f:
        json.dump(Header_str,f,indent=None)
    

#Used this to help me understand the different terminologies: https://www.geeksforgeeks.org/important-blockchain-terminologies/?ref=gcse
'''class Block:
    def __init__(self):
        self.chain = list()
        genesis_block = None


    def new_block(self, proof, former_hash):
        block = {'index': ,
                 'timestamp': ,
                 'proof': proof,
                 'former_hash': former_hash}
        self.chain.append(block)
        return block
    
    def hash(self, block):
        hashlib.sha256(Data_str.encode('utf-8')).hexdigest()'''
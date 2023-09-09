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

@dataclass
class Block:
    header: dict[str:str]
    body: dict[str:list[dict]]

class processed_transaction:
    
    def __init__(self,Height,Current_File,Previous):
        self.height=Height
        self.current_file=Current_File
        self.previousblock=Previous
        
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
    # Used this to help me understand the different terminologies: https://www.geeksforgeeks.org/important-blockchain-terminologies/?ref=gcse

    def process(self):
        folder_name="../pending/"
        current_time=datetime.datetime.now()
        Timestamp=int(datetime.datetime.timestamp(current_time))
        body_list=[]

        with open(folder_name + self.current_file + ".json","r") as f:
            body_dict={"hash":self.current_file,"content":f.read()}
            body_list.append(body_dict)
            print(body_dict)

        if(self.height==0):
            self.previousblock="NA"
        else:  
            with open(folder_name + self.previousblock + ".json","r") as f:
                body_dict={"hash":self.previousblock,"content":f.read()}
                body_list.append(body_dict)
                print(body_dict)

        #copy the this file into the processed folder and delete the file from pending
        #https://stackoverflow.com/questions/123198/how-to-copy-files
        body={"body":body_list}
        body_str=str(body)
        body_str=body_str.replace(" ","")
        Hash=hashlib.sha256(body_str.encode('utf-8')).hexdigest()
        
        header_dict={
            "height": self.height,
            "timestamp":Timestamp,
            "previousblock":self.previousblock,
            "hash":Hash
        }

        header={"header":header_dict}
        Header_str=str(header)
        Header_str=Header_str.replace(" ","")
        blocks="../blocks/"
        file_name=hashlib.sha256(Header_str.encode('utf-8')).hexdigest()

        
        block=str(Block(header=header,body=body))
        block=block.replace(" ","")

        with open(blocks + file_name + ".json","w") as f:
            json.dump(block,f,indent=None)
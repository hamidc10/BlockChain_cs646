import datetime
import json
import hashlib



# TASK for Block file
# Similar to a transaction, a block should be treated as an object that can be stored as a .json file. 
# The block should be made up of two main parts, a header and a body.  The body should include a list/array of transactions included in the block.  
# The header should include the following:
# Block height(the order the block was created, initial block would be height 0, next block would be height 1, etc..)
# Timestamp
# Hash of the Previous Block (for a block of height 0 you can just use "NA")
# Hash of the Block Body for the current block 
# When the file is saved, hash the header content only and use the resulting hash as the name of the file. 


#Used this to help me understand the different terminologies: https://www.geeksforgeeks.org/important-blockchain-terminologies/?ref=gcse
class Block:
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
        hashlib.sha256(Data_str.encode('utf-8')).hexdigest()

    



 
    



    



 
    


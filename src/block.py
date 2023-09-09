import datetime
import json
import hashlib
import os
import shutil


# TASK for Block file
# Similar to a transaction, a block should be treated as an object that can be stored as a .json file.
# The block should be made up of two main parts, a header and a body.  The body should include a list/array of transactions included in the block.
# The header should include the following:
# Block height(the order the block was created, initial block would be height 0, next block would be height 1, etc..)
# Timestamp
# Hash of the Previous Block (for a block of height 0 you can just use "NA")
# Hash of the Block Body for the current block
# When the file is saved, hash the header content only and use the resulting hash as the name of the file.


class processed_transaction:
    
    def __init__(self):
        self.file_list = []

    def add_transaction(self, file_name):
        self.file_list.append(file_name)

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
        pending = "../src/pending/"
        processed = "../src/processed/"
        blocks = "../src/blocks/"
        block_list = []
        for file in self.file_list:
            # print(file)
            current_time = datetime.datetime.now()
            Timestamp = int(datetime.datetime.timestamp(current_time))
            body_list = []
            with open(pending + file + ".json", "r") as f:
                body_dict = {"hash": file, "content": json.loads(f.read())} 
                # https://www.geeksforgeeks.org/how-to-read-dictionary-from-file-in-python/
                body_list.append(body_dict)
                
            height = self.file_list.index(file)
            # print(height)
            if height == 0:
                previousblock = "NA"
            else:
                previousblock = block_list[height - 1]
                with open(blocks + previousblock + ".json", "r") as b:
                    body=json.loads(b.read())
                    # body_dict = {"hash": self.file_list[height-1], "content": b.read()}
                    # Used to help with cleaner function
                    # https://www.learndatasci.com/solutions/python-typeerror-sequence-item-n-expected-string-list-found/
                    cleaner=(map(str,(body["body"])))
                    body_list.append(','.join(cleaner))
                
            # copy the this file into the processed folder and delete the file from pending
            # https://stackoverflow.com/questions/123198/how-to-copy-files
            # body={"body":body_list}
            body_str = str(body_list)
            body_str = body_str.replace(" ", "")
            Hash = hashlib.sha256(body_str.encode("utf-8")).hexdigest()

            header_dict = {
                "height": height,
                "timestamp": Timestamp,
                "previousblock": previousblock,
                "hash": Hash,
            }

            # header={"header":header_dict}
            header_str = str(header_dict)
            header_str = header_str.replace(" ", "")
            file_name = hashlib.sha256(header_str.encode("utf-8")).hexdigest()

            block = {"header": header_dict, "body": body_list}
            print(block)
            
            with open(blocks + file_name + ".json", "w") as f:
                json.dump(block, f, indent=None)

            block_list.append(file_name)

            # https://www.geeksforgeeks.org/how-to-move-all-files-from-one-directory-to-another-using-python/
            src_path = os.path.join(pending, file+".json")
            dst_path = os.path.join(processed, file+".json")
            test=shutil.move(src_path, dst_path)
          
            

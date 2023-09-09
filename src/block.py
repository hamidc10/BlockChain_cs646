import datetime
import json
import hashlib
import os
import shutil


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

    def new_block(self, file_name):
        """
        Recieves the file_name that it is to be added to the block.
        Once the data is received it then get put into a dictionary called 'block' as a value to the 'body' key. 
        The block is then converted to JSON.
        Used this for help with JSON writing to file:
        -https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/

        """

        self.file_hash_list.append(file_name)

        pending = "./src/pending/"
        processed = "./src/processed/"
        blocks = "./src/blocks/"

        current_time = datetime.datetime.now()
        timestamp = int(datetime.datetime.timestamp(current_time))
        body_list = []

        # Reference used to learn how to read json file content as a dictionary:
        # https://www.geeksforgeeks.org/how-to-read-dictionary-from-file-in-python/

        # Creating the body for the block based on the current transaction.
        with open(pending + file_name + ".json", "r") as f:
            body_dict = {"hash": file_name, "content": json.loads(f.read())}
            body_list.append(body_dict)

        height = self.file_hash_list.index(file_name)
        if height == 0:
            previousblock_hash = "NA"
        else:
            previousblock_hash = self.block_hash_list[height - 1]

            #  Appending body of previous block to body of current block.
            with open(blocks + previousblock_hash + ".json", "r") as b:
                body = json.loads(b.read())
                body_list.append(body["body"])

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
        if self.print_block == "Y":
            print(block)

        with open(blocks + block_name + ".json", "w") as new_block:
            json.dump(block, new_block, indent=None)

        self.block_hash_list.append(block_name)

        # Moving the processed transaction file into the processed folder and deleting the file from the pending folder.
        # https://www.geeksforgeeks.org/how-to-move-all-files-from-one-directory-to-another-using-python/
        src_path = os.path.join(pending, file_name + ".json")
        dst_path = os.path.join(processed, file_name + ".json")
        shutil.move(src_path, dst_path)

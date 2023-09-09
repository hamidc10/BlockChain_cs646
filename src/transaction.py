import json
import datetime
import hashlib


class Transaction_info:
    def __init__(self):
        pass

    # This gets the user input to get ready to put into a JSON format
    # Once the user data is received it then get put into a dictionary which would be converted to JSON
    # Used this for help with JSON writing to file:
    #    -https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/

    # Before we save the file we need to hash it by using SHA256
    # I took the dictionary and make it into a str with no space then I can hash it using hashlib library
    # After we hash it, The file for the JSON will be saved as hash we created
    # Used this to help me understand how hashlib worked
    #   -https://docs.python.org/3/library/hashlib.html
    # I had an error with "String must be encoded" found this to help
    #   -https://bobbyhadz.com/blog/python-typeerror-strings-must-be-encoded-before-hashing

    def new_transaction(self):
        From = input("From who:")
        To = input("To who:")
        Amount = input("What is the amount:")
        current_time = datetime.datetime.now()
        Timestamp = int(datetime.datetime.timestamp(current_time))

        Data = {"Timestamp": Timestamp, "From": From, "To": To, "Amount": Amount}

        Data_str = str(Data)
        Data_str = Data_str.replace(" ", "")
        folder_name = "./src/pending/"
        file_name = hashlib.sha256(Data_str.encode("utf-8")).hexdigest()

        with open(folder_name + file_name + ".json", "w") as f:
            json.dump(Data, f, indent=None)

        return file_name

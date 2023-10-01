import os
import json
import datetime
import hashlib

from constants import pending_transactions_folder

# Note: converted this back to a function because it doesn't really need to be a class
def new_transaction(from_address: str, to_address: str, amount: int, signature: str, sender_address:str, sender_pbk: str) -> str:
    """
    Creates a transaction file with the given information in the pending folder
    and returns the hash of the created transaction.
    """
    current_time = datetime.datetime.now()
    timestamp = int(datetime.datetime.timestamp(current_time))
    data = {
        "Timestamp": timestamp,
        "From": from_address,
        "To": to_address,
        "Amount": amount,
        "Signature": signature,
    }
    
    # Dictionary with transaction information and the name of sender
    complete_transaction = {"transaction": data,"details":sender_address, "public_key":sender_pbk}
    
    complete_transaction_str = str(complete_transaction).replace(" ", "")
    complete_hash = hashlib.sha256(complete_transaction_str.encode("utf-8")).hexdigest()
    file_name = complete_hash + ".json"

    file_path = os.path.join(pending_transactions_folder, file_name)
    with open(file_path, "w") as f:
        json.dump(complete_transaction, f, indent=None)
        
    return complete_hash

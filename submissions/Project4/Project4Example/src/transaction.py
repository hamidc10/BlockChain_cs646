# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 11/10/23

import os
import json
import datetime
import hashlib
from typing import List


def new_transaction(
    from_address: str,
    to_address: str,
    amount: int,
    signature: bytes,
    public_key_file_path: str,
    transaction_folders: List[str],
) -> str:
    """
    Creates a transaction file with the given information in the given folders
    and returns the hash of the created transaction.
    """
    current_time = datetime.datetime.now()
    timestamp = int(datetime.datetime.timestamp(current_time))
    data = {
        "Timestamp": timestamp,
        "From": from_address,
        "To": to_address,
        "Amount": amount,
        "Signature": signature.hex(),  # have to convert to hexadecimal format to save as JSON
        "PublicKeyFilePath": public_key_file_path,  # the Block class needs the public key to validate the signature
    }
    data_str = str(data).replace(" ", "")
    data_hash = hashlib.sha256(data_str.encode("utf-8")).hexdigest()
    file_name = data_hash + ".json"
    for folder in transaction_folders:
        file_path = os.path.join(folder, file_name)
        os.makedirs(folder, exist_ok=True)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=None)
    return data_hash

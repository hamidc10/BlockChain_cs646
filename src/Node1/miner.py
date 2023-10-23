import json
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

from constants import (
    keys_folder
)

amount=0
class verify:
    def miner_verify(file_path):
        global amount
        f = open(file_path, "r+")
        transaction_body = json.loads(f.read())
        garbage_message = json.dumps({"j": "jkl"}).encode("utf-8")
        # replace data_to_verify below with garbage message to see what happens if unable to verify
        
        try:
            # https://www.w3schools.com/python/gloss_python_check_if_dictionary_item_exists.asp
            # https://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python

            # Checking transaction only has the expected keys: timestamp, from, to, amount, signature
            transaction_keys = transaction_body.keys()
            # print(transaction_keys)
            should_only_have_keys = ["Timestamp", "From", "To", "Amount", "Signature"]
            if not all(keys in transaction_keys for keys in should_only_have_keys):
                print(transaction_keys, "\n", f"dict_keys({should_only_have_keys})")
                print("Transaction format wrong!")
                raise Exception("Transaction format wrong!")
            
            wallet_address = transaction_body["From"]
            public_key_file = f"{keys_folder}"+f"{wallet_address}.pem"
            
            # Validate transaction on blockchain
            pem = open(public_key_file, "rb")
            public_key = serialization.load_pem_public_key(pem.read())

            # Recreating data from transaction for verification 
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
            # print("This is the file path",file_path)
            
            f.close()
            print("This is updated_ transaction",transaction_body)
            reward_finder=transaction_body["Amount"]
            print(reward_finder)
            reward=0.0001*reward_finder
            amount+=reward
            new_amount=reward_finder-reward
            transaction_body.update({"Amount": new_amount})
            print(transaction_body["Amount"])
            
            with open(file_path,"w") as f2:
                json.dump(transaction_body,f2, indent=None)
            
            
            return True
        except Exception as e:
                print(e)                
                print("Unable to add transaction: Transaction DENIED")
                return False
        # finally:
        #     f.close()
        

# def miner_reward(file_path):
#     global amount
#     if verify.miner_verify(file_path) == True:
#         reward_reader=json.loads(open(file_path, "r").read())
#         reward_finder=reward_reader["Amount"]
#         reward=0.0001*reward_finder
#         amount+=reward
#         print(amount)

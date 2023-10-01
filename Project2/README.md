# Group 3

###### By: Hamid Choucha, Chantel Rose Walia, Xavier Martinez, Vira Shankar, Trey Carroll 
  
---------------------------------------------------------------------------------------------------

## Blockchain Project 2

### How to Test

First make sure to make sure that you pip install -r requirements.txt

Once that is done then you want to make sure that you are in the right folder in order to run the code:

* Make sure that you first cd into src folder then you can run python or python3 depending on your terminal main.py

From there you will be asked a series of prompts make sure to follow the prompts and type in the correct response so either (y/n) or (1,2,3) or an amount that needs you want to send.

If you are done with the code then ctrl-c to then stop.

## Components for Project2

### account_state.py

This python file is created to help assist in the following:
- Storing of current balances for each wallet. 
- Assist user check other peoples balances.

**Goal** of the file is to store/update the balance of the three wallets using type Dict, done in ```block.py``` , and make them easily accessible to be read by ```wallet.py``` (in each wallet directory).

* There are three functions that have been created:
    * *init_account_state* :
        * This function helps to create an empty account balance json file so that it can then save the current balances of users.
    * *load_account_state* :
        * load account state goal is to grab information form the AccountStateDict and read the json file
    * *save_account_state* :
        * This functions updates the json file and writes what the new account balances are for the correct wallet after a valid transaction has occurred

### block.py

This python file is created to make blocks on the blockchain. It won't make a block if the transaction is not validated.

**Goal** for the file is to take transactions from the *pending* folder, where they are stored as a JSON file. The code takes in the information from the transaction and stores them as a dictionary value to help assist in verifying the transaction by using the *public_key.verify()* from the *cryptography library* to validate the signature. In order to validate the signature, it needs to check the public key from the sender, if the signature does not match the format checker or if the transaction is in the incorrect format i.e wrong keys, in the try catch it will provide the error with a message that reads:"**Unable to add transaction to block: Transaction DENIED**".

* There are 2 functions that have been created:

    * *init*:
        * It helps to initialize three variables that will be used by new_block(). Such as the the file_hash_lst, block_hash_lst, and print_block. This helps establish variables to store the transaction json , the block json, and a flag to help print the block incase the user wants to check the block to ensure it worked properly.

    * *new_block*:
        * It gets the information from the Json file from the transaction , it then verifies the signature of the sender of the transaction amount. If the transaction amount is valid and the From ,To , and Amount are also satisfied it will then create a new block if one does not exist or will add to the existing block chain with all the information. if the transaction information it received is wrong then it will display an error message to the user and will not add that faulty block to the chain, the transaction will remain in the *pending* folder and will never be processed. If the transaction is verified, the block is added/created and the transaction json is moved from *pending* to *processed*.

### constants.py

This python file is created to help keep and store file paths, to help ease with reading and writing files.

### transaction.py

This python file is created to help keep and store the transaction information between wallets into a dictionary called *data*. *Data* has the Timestamp, From, To, Amount and Signature information. It recieves all the information and aptly stores it in *data*. A hash is created from the dictionary and used as the transaction file name: *hash_of_transaction*.json

**Goal** Is to store the transaction information in the *pending* folder in order for ```block.py``` to read and verify it and add it to the blockchain.

* There is 1 function that has been created:
    * *new_transaction*:
        * It takes in From_address(str), To_address(str), Amount(int), Signature(str). From there it will organize the information into the data dictionary and add a Timestamp. Once it has create the dictionary it will then write the Json file and return the hash of the transaction so it can then go to the pending folder to wait to get processed.

### wallet_skeleton.py

*This is the skeleton for each "Wallet" that we create. A copy of it is added to each wallet directory upon running the code (if the wallet directories don't already exist).*

This python file is created to help create the wallet structure for each wallet by creating the private_key, deriving the public key from the private key and address of the wallet by hashing the public key. This all is acheived by using the *cryptography library*. It also allows the user to send and check their or another users balance.

**Goal**:   Allow the user to send, and check their balance as well as other wallets balances.

* There are 3 functions that have been created:
    * *init*:
        * Inside this function we, initialize the name of the wallet, generate the private key and store it within the wallet directory as *private.pem*, generate the public key from the private key, the address of the wallet is initialized as the hash of the public key, and finally the public key is stored in another folder called *public_keys* as *wallet_address*.pem.

    * *send*:
        * Uses the "from_address","to_address" and "amount" as well as the private key in order to then create a signature that contains the From, To, Amount information. It then sends the from_address, to_address, amount, and the signature to transaction.py which returns the hash of the transaction generated, which is then returned by send() back to main.py. 

    * *check_balance*:
        * The check balance uses the address of the wallet to then call account_state.py in order to check the current balance of the wallet. If there is no transaction then it will return a balance of 0.

### main.py

This python file is created to run the previous python files mentioned and prompt the user with certain questions based on their inputs.

**Goal**:   Allow the user to make transactions between wallets and to let the user check their and other wallets balance.

* There are 2 functions that have been created:
    * *init_dirs*:
        * This function allows to create the three wallets as well as *blocks*, *pending*, *processed*, and *public_keys* folder if they do not already exist. It also helps to create the wallet.py- that has been derived from wallet_skelton.py, inside each Wallet folder. 

    * *main*:
        * This function is where the user can select which wallet they want to *"be in control of"* to send transaction, check that wallets balance or select the other two wallets to view their balance.
        The user will just follow what the function ask usually to input a number between 1-3 or enter a desired amount to send to another wallet

**Links used:**

* From Project2
    1. <https://www.geeksforgeeks.org/python-import-module-from-different-directory/>
    2. <https://note.nkmk.me/en/python-os-mkdir-makedirs/>
    3. <https://www.geeksforgeeks.org/python-os-mkdir-method/>
    4. <https://stackoverflow.com/questions/42339876error-unicodedecodeerror-utf-8-codec-cant-decode-byte-0xff-in-position-0-in>
    5. <https://www.geeksforgeeks.org/how-to-read-dictionary-from-file-in-python/>
    6. <https://www.w3schools.com/python/gloss_python_check_if_dictionary_item_exists.asp>
    7. <https://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python>
    8. <https://www.geeksforgeeks.org/how-to-move-all-files-from-one-directory-to-another-using-python/>
    9. <https://cryptography.io/en/latest/hazmat/primitives/asymmetric/rsa/>
    10. <https://www.educative.io/answers/how-to-create-digital-signature-in-python-using-ecdsa-signingkey>
                (was not used but help answer some questions)

* From Project1
    1. <https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/>
    2. <https://docs.python.org/3/library/hashlib.html>
    3. <https://bobbyhadz.com/blog/python-typeerror-strings-must-be-encoded-before-hashing>
    4. <https://www.geeksforgeeks.org/important-blockchain-terminologies/?ref=gcse>
    5. <https://www.learndatasci.com/solutions/python-typeerror-sequence-item-n-expected-string-list-found/>
    6. <https://stackoverflow.com/questions/123198/how-to-copy-files>
    7. <https://www.geeksforgeeks.org/how-to-move-all-files-from-one-directory-to-another-using-python/>
    8. <https://www.geeksforgeeks.org/how-to-read-dictionary-from-file-in-python/>

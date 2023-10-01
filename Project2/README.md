# Blockchain Project 2

## How to test

First make sure to make sure that you pip install -r requirements.txt

Once that is done then you want to make sure that you are in the right folder in order to run the code:

* Make sure that you first cd into src folder then you can run python or python3 depending on your terminal main.py

From there you will be asked a series of prompts make sure to follow the prompts and type in the correct response so either (y/n) or (1,2,3) or an amount that needs you want to send.

If you are done with the code then ctrl-c to then stop.

## Components for Project2

### Account state file

This python file is created to help assist in the storing of user current balances as well as help in assist user check other peoples balances.

**Goal** of the file is to store the balance of the three wallets using type Dict, and make them easily accessible to be read by wallet.py. This makes it show up within the main class, so that when the prompts are followed or a transaction is sent, it was able to be printed.

* There are three functions that have been created:

    1. *init_account_state*
        * This function helps to create an empty account balance json file so that it can then save the current balances of users.
    2. *load_account_state*
        * load account state goal is to grab information form the AccountStateDict and read the json file
    3. *save_account_state*
        * This functions updates the json file and writes what the new account balances are for the correct wallet after a valid transaction has occurred

### Block

This python file is created to make blocks on the blockchain. It won't make a block if the transaction is not validated.

**Goal** for the file is to take transactions from the pending and processed transaction folders, and to store them as a JSON file. The code takes in the information from the transaction and stores them as a dictionary value to help assist in checking that the transaction is valid after using the *cryptography library to valid the signature*. In order to valid the signature it needs to check the public key from the sender and if the signature does not match the format checker in the try catch it will provide the error with a message that reads:"**Unable to add transaction to block: Transaction DENIED**".

* There are Two functions that have been created:

    1. *init*
        * It helps to initialize three variables that will be used by newblock. Such as the the file_hash_lst, block_hash_lst, and print_block. These variables help establish variables to store the transaction json , the block json, as well a function to help print the block incase the user wants to check the block to ensure it worked properly.

    2. *newblock*
        * It gets the information from the Json file from the transaction , it then verifies the signature of the sender of the transaction amount. If the transaction amount is valid and the From ,to , and amount are also satisfied it then will create a new block if one does not exist or will add to the existing block with all the information. The transaction information it received is wrong then it will display an error message to the user and will not add that faulty block to the chain.

### Constants

This python file is created to help keep and store  file paths just to help ease with reading and writing files.

### Transaction

This python file is created to help keep and store the transaction information between wallets into two dictionary. The first dictionary has the Timestamp,From,To,Amount and signature information that it will send to Block.py to then verify the information and add it if it passes. The second dictionary has the pervious information as well as the the public key of the sender and the address of the wallet that the transaction has been sent from.

**Goal** Is to send the transaction information to the block in order for teh block to verify it and add it to the blockchain.

* There is one function that has been created:
    1. *new_transaction*
        * It takes in From_address(str), To_address(str), Amount(int), Signature(str), sender_address(str), sender_public_key (str). From there it will organize the information into the appropriate dictionary as well as add a Timestamp. Once it has create the two dictionaries it will then write the Json file and return the complete has of the transaction so it can then go to the pending folder to wait to get processed.

### Wallet Skeleton

This python file is created to help create the wallet structure for each wallet by creating the private_key, deriving the public key from the private key, address of the wallet by using the*cryptography library*. It also allows the user to send and check there balance.

**Goal**  Allow the user to send, and check there balance as well as other users wallets balances.

* There are Three functions that have been created:
    1. *init*
        * Inside this function we initialize the name of the wallet, the address of the wallet, the signature of the user of that wallet, as well as details which has the public key information. It allows the wallet to create a private.pem file that contains the private key. Once the private key is created then we can derive the public key in order to generate the address by hashing the public key.

    2. *send*
        * Uses the address,and amount in order to then create a signature that contains the message that has From, To, Amount information to then salt and hash it to create th signature. It then returns the address, public_key, to_address, from_address, amount, and the signature for it to then be used by transaction.py.

    3. *check_balance*
        * The check balance uses the address of the wallet to then call account_state.py inorder to check the current balance of the wallet. If there is no transaction then it will return a balance of 0.

### Main

This python file is created to run the previous python files mentioned and prompt the user with certain questions based of there inputs.

**Goal**  The Overall goal is to allow send valid transaction that have been validated to the blockchain. Then verify the amount inside the the users wallet and allow the user to check other wallets balance amounts.

* There are two functions that have been created:
    1. *init_dirs*
        * This function allows to create the three wallets as well as blocks,pending,processed, and public_keys folder if they do not already exist.It also helps to create the wallet.py inside each Wallet folder that has been derived from wallet_skelton.py

    2. *main*
        * This function is where the user can select which wallet they want to "be in control of to send transaction, check that wallets balance or select the other two wallets inorder to view there balance.
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

# Blockchain Project 2

## How to test

* install the requirements in requirements.txt
* run main.py from the src/ folder and follow the prompts

## Components

### Account state file

stores the current balances of all blockchain users

* only transactions with valid signatures are counted
* maintained by the Block class
* read by the Wallet class

### Wallet class

provides a user with access to the blockchain

* allows a user to create transactions
* allows a user to check their own account balance (by reading the account state file)
* allows a user to check another user's account balance (by reading the account state file)

### Block class

processes transactions created by users (via the Wallet class)

* validates the signatures of senders
* saves validated transactions to blockchain
* updates user balances in the account state file

## Files

### main.py

lets the user run a test simulation with 3 different wallets on the blockchain

### block.py

has a Block class with functionality of a node that validates transactions and adds them to the blockchain

### wallet.py

has a Wallet class with functionality of a wallet that interacts with the blockchain

### transaction.py

has functions for creating transactions (used by wallet.py)

### account_state.py

has functions for loading and saving the account state file (used by block.py and wallet.py)

### constants.py

has variables for the file paths used by all the code

## Libraries

### pycryptodome

https://pycryptodome.readthedocs.io/en/latest/index.html

used for:

* creating RSA wallet keys
* creating transaction signatures
* validating transaction signatures

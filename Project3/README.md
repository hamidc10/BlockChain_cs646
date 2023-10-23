# Blockchain Project 3

## How to test

* run `python3 -m node1.main` from the Project3 directory in a separate terminal
* run `python3 -m node2.main` from the Project3 directory in a separate terminal
* run `python3 -m node3.main` from the Project3 directory in a separate terminal
* run `python3 -m main` from the Project3 directory in a separate terminal and follow the prompts

## Known issues

* account state file is not always accurate because of conflicts when multiple nodes update it at the same time
* block heights are not always accurate after restarting the nodes

## Bonus

we did 2 bonus tasks:

* miners take turns creating blocks (random choice)
* defined a protocol for node communication (described below)

## Blockchain socket communication protocol (bonus)

For syncing transactions and blocks between nodes

Each block/transaction file is sent using the following 3-part message protocol:

1. Send the file type as a message ("TRANSACTION" or "BLOCK")
2. Send the file name as a message (so the client knows what to save it as)
3. Send the file content as a message

Each message is made up of 4 sends/receives on the socket:

1. The server sends the message size (so the client knows how big of a buffer to use)
2. The client confirms that it received the message size
3. The server sends the message content
4. The client confirms that it received the message content

Connection logs are printed and saved to log files.

## Components

### Account state file

stores the current balances of all blockchain users

* only transactions with valid signatures are counted
* maintained by the Node class
* read by the Wallet class

### Wallet class

provides a user with access to the blockchain

* allows a user to create transactions
* allows a user to check their own account balance (by reading the account state file)
* allows a user to check another user's account balance (by reading the account state file)

### Node class

processes transactions created by users (via the Wallet class)

* validates the signatures of senders
* saves validated transactions to blockchain
* updates user balances in the account state file
* syncs transactions and blocks between nodes with the help of NodeConnector class

## Files

### main.py

lets the user run a test simulation with 3 different wallets on the blockchain

### node.py

has a Node class with functionality of a node that validates transactions and adds them to the blockchain

### connector.py

has a NodeConnector class with functionality of the socket communication protocol

### wallet.py

has a Wallet class with functionality of a wallet that interacts with the blockchain

### transaction.py

has functions for creating transactions (used by wallet.py)

### account_state.py

has functions for loading and saving the account state file (used by node.py and wallet.py)

### constants.py

has variables for the file paths used by all the code

# Blockchain Project 4

## How to test

* run `python3 -m node1.main` from the Project3 directory in a separate terminal
* run `python3 -m node2.main` from the Project3 directory in a separate terminal
* run `python3 -m node3.main` from the Project3 directory in a separate terminal
* run `python3 -m main` from the Project3 directory in a separate terminal and follow the prompts

after running a few tests, you can see that:

* coinbases are created for each node
* transactions and blocks are synced between nodes (in node1, node2, node3 folders)
* account state for nodes and test wallets is updated (account_state.json)
* node logs are printed in the node terminals showing transactions validated and blocks created
* node socket logs are saved to socket.log file in node1, node2, node3 folders

## Changes from project 3

### How we are validating blocks

TODO: document this (Trey)
read PLAN.md for details

### How we are making nodes compete

TODO: document this (Xavier)
read PLAN.md for details

### How we are handling/preventing forks

TODO: document this (Xavier)
read PLAN.md for details

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
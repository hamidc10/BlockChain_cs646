# Blockchain Project 4

## How to test

* Run `python3 -m main` from the Project4 directory and create some pending transactions
* Run `python3 -m node1.main` from the Project4 directory in a separate terminal to start node1
* Run `python3 -m node2.main` from the Project4 directory in a separate terminal to start node2
* Run `python3 -m node3.main` from the Project4 directory in a separate terminal to start node3
* Watch the logs in the node terminals to see:
  * the nodes create coinbases
  * the nodes compete to mine each transaction
  * the nodes handle forks when they occur
  * the nodes sync blocks between each other
* Node socket logs are saved to `socket.log` in each of the node folders
* Wallet balances are stored in `account_state.json`

## Changes from project 3

### How we are validating blocks

* Each block received from a different node is validated with the checks listed on Canvas
* See the `validate_block` method in the `node.py`

### How we are making nodes compete

* New transactions are sent to each node's pending folder
* Proof of work puzzle logic is implemented in the Node class
  * The node that solves the puzzle in the shortest amount of time / with the smallest nonce value wins and gets to mine the block
  * The target is to generate a hash from the previous block that starts with one leading zero ("0")
  * The target can be increased by editing the `solve_puzzle` method in `node.py`

### How we are preventing/handling forks

#### Prevention

* Each node continuously checks for competing blocks and abandons mining the current block if another node mined it faster
* That way, there is a very low chance for forks to be created
* Each node will process the same transaction at the almost the same time
* A random UUID is added to each node's version of the block in the puzzle algorithm to ensure they don't produce the same hashes / winning nonce values
* If multiple nodes finish mining and sending a block at the same time, only the one with the smallest nonce value will be kept
* If multiple blocks are tied with the smallest nonce value, the block with the first alphabetically sorted block hash wins

#### Handling

* A fork is detected when a node fails to send its block to another node
* There are two possible reasons for a fork:
  * Another node is trying to send to us at the same time. In this case, we need to handle the fork by:
    * Receive blocks from the other nodes
    * Pick the winning block from all of the received blocks and our own
    * If the winning block is ours, try sending it to the other nodes again
    * If the winning block is not ours:
      * Delete our block file
      * Remove our block hash from our hash list
      * Accept the winning block
  * We have fallen behind all the other nodes because they have finished processing all pending blocks (for now)
    and they won't accept our connections until a new transaction comes. In this case, we need to handle the fork by:
    * Abandon our block and fetch blocks from another node

## Known problems

* Sometimes the account state is slightly inaccurate because two nodes might finish mining a block at the same time and both update the account state
* We have minimized this issue as much as possible, but it is not perfect all the time

## Components

### Account state file

Stores the current balances of all blockchain users

* Only transactions with valid signatures are counted
* Maintained by the Node class
* Read by the Wallet class

### Wallet class

provides a user with access to the blockchain

* Allows a user to create transactions
* Allows a user to check their own account balance (by reading the account state file)
* Allows a user to check another user's account balance (by reading the account state file)

### Node class

processes transactions created by users (via the Wallet class)

* Validates the signatures of senders
* Saves validated transactions to blockchain
* Updates user balances in the account state file
* Syncs transactions and blocks between nodes with the help of NodeConnector class
* Competes to mine blocks and handles forks

## Files

### `main.py`

Lets the user run a test simulation with 3 different wallets on the blockchain

### `node.py`

Has a Node class with functionality of a node that validates transactions and adds them to the blockchain

### `connector.py`

Has a NodeConnector class with functionality of the socket communication protocol

### `wallet.py`

Has a Wallet class with functionality of a wallet that interacts with the blockchain

### `transaction.py`

Has functions for creating transactions (used by `wallet.py`)

### `account_state.py`

Has functions for loading and saving the account state file (used by `node.py` and `wallet.py`)

### `constants.py`

Has variables for the file paths used by all the code

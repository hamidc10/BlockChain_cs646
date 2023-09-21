# Blockchain Project 2

## How to test

run main.py and follow the prompts

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

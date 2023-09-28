# Blockchain Project 2

## How to test

run main.py and follow the prompts

* 1st prompt will ask if the user wants to print blocks to terminal. in test cases we said n.
* second prompt will ask the user to check a wallet or create a wallet.
* 3rd prompt will ask the user if they want to create a transaction or check balances of their own or someone elses wallet.
* if transaction is selected, it will ask you to choose a wallet to send to, followed by how much.
* it will then return the completed transaction followed by the digital signature.

* if check account balance is selected, it will return the account balance then repeat the code.

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

* Also added cryptography hazmat primitives. This allows us to implement authenticated encryption, Symmetric encryption, symmetric padding, and message digests. We use this to serialize and digest signatures and keys, because we need to encrypt them into a hash when initializing a transaction to another wallet. Goal is to read account state, retrieve private keys, and determine whether a transaction is able to be sent or not. It reads account state to determine the balances of wallet1, wallet2, and wallet3. It then uses cryptography.hazmat.primitives to serialize and hash the private keys and then generate digital signatures to sign transactions that have occurred. For example, if you send 1 btc to wallet2, it should print out self.signature to sign the transaction.

### Block class

processes transactions created by users (via the Wallet class)

* validates the signatures of senders
* saves validated transactions to blockchain
* updates user balances in the account state file

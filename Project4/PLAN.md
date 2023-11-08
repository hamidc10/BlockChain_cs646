# PLAN

## summary of changes

### making nodes compete to process each transaction

- new transactions must be sent to each node's pending folder
- proof of work puzzle logic must be implemented in the Node class
  - the node that solves the puzzle in the shortest amount of time / with the smallest nonce value wins and gets to mine the block

### handling forks

- we can make each node continuously check for competing blocks and abandon mining the current block if another node mined it faster
- that way, there is a very low chance for forks to be created
- each node will process the same transaction at the almost the same time
- if multiple nodes finish mining and sending a block at the same time, only the one with the smallest nonce value will be kept

### validating blocks from other nodes

- each block received from a different node must be validated with the checks listed on Canvas

## team work

everyone has individual functions to create / changes to make - due next Friday (Nov 3) by 10pm

everyone has their own branch to make changes on

after next Friday (Nov 3), i will merge everyone's branches together and make sure they work together, then i will submit before the project due date

since most changes depend on other changes, each team member branch is not expected to fully work until i merge them all together

### Vira tasks (branch: vira and main)

driver code changes:

- send transactions to all nodes
- in the root main.py, when a transaction is created, instead of picking a random node folder to put the transaction file, put it in all 3 node folders

Connector class (socket functions) changes:

- file receiving and saving should be separate so that files can be checked before saving
- transaction files no longer need to be sent

Node class `run` method changes:

- pick up the first transaction file found in the pending folder
- if a file is found, call `self.new_block()`
- if a block was mined, send it to the other nodes
- sleep for 1 second

Node class `new_block` method changes:

- move transaction validation code into a separate method that can be reused

other Node class changes:

- add `self.previous_block` value

### Chantel tasks (branch: chantel)

Node class `new_block` method changes:

- call `self.solve_puzzle()` at the beginning
- if result is True, we won the puzzle, continue creating block (+ set "nonce" in header)
- if result is False, we lost the puzzle, abandon creating block (so return None early)

Node class `solve_puzzle` method (NEW):

- set a random number value in `self.previous_block` to prevent previous block hashes from being identical for all nodes
- initialize a nonce value at 0
- in a while loop:
  - first check for competing blocks from other nodes:
    - if `self.check_for_competing_blocks()` returns any blocks:
      - pass the result of `self.pick_winning_block()` to `self.accept_winning_block()` to save winning block
      - return a tuple with False (to indicate that we lost) and 0
  - attempt to solve the puzzle with the current nonce value:
    - see video in TA corner
    - using `self.previous_block`, set the block "nonce" value to be the current nonce value
    - take a hash of the block
    - if the hash starts with "0000" (target of 4 zeros), we have found a winning nonce value
      - return a tuple with True (to indicate that we won) and the winning nonce value
  - increment the nonce value

### Hamid tasks (branch: hamid)

Node class `check_for_competing_blocks` method (NEW):

- create empty list to store competing blocks
- for each other node:
  - attempt to receive a block (use `self.receive_processed_block()`)
  - if a block is received:
    - if the block is valid (use `self.validate_block()`):
      - add the block to the competing blocks list
- return the list of competing blocks

Node class `accept_winning_block` method (NEW):

- given the winning block object
- save the result of `self.pick_winning_block()` in the blocks folder (`self.blocks_folder`)
- set the block as `self.previous_block`
- add the block hash to `self.block_hash_list`
- call `self.save_node_state()`
- move the associated transaction file from the pending folder (`self.pending_transactions_folder`) to the processed folder (`self.processed_transactions_folder`)

### Trey tasks (branch: trey)

Node class `validate_block` method (NEW):

(validation checks from Canvas)

you can use `self.validate_transaction()` to validate the transactions again

document validation of blocks in README

### Xavier tasks (branch: xavier)

Node class `pick_winning_block` method (NEW):

- given a list of block objects
- return the block that has the smallest "nonce" value in its header

document other changes compared to project 3 in README:

- how we are making nodes compete
- how we are handling/preventing forks

# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 9/10/23

from transaction import Transaction
from block import Block


# Driver code
def main():
    print("Project 1 by Group 3\n")
    print_block = input("Enable Printing Block Made to Terminal? (Y/n):")
    transaction = Transaction()
    block = Block(print_block)

    while True:
        print("\n--- Menu ---")
        print("1. Add Transaction")
        print("2. Exit")
        choice = input("Input # of your choice:")

        if choice == "1":
            file_name = transaction.new_transaction()
            block.new_block(file_name)
        elif choice == "2":
            exit(1)


if __name__ == "__main__":
    main()

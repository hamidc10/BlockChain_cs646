from transaction import Transaction_info
from block import processed_transaction


def main():
    print("Project 1 by Group 3")
    print_block = input("Enable Printing Block Made to Terminal? (Y/n):")
    transaction = Transaction_info()
    block = processed_transaction(print_block)

    while True:
        print("--- Menu ---")
        print("1. Add Transaction")
        print("2. Exit")
        choice = input("Input # of your choice:")
        
        if choice == "1":
            file_name = transaction.new_transaction()
            block.process(file_name)
        elif choice == "2":
            exit(1)


if __name__ == "__main__":
    main()

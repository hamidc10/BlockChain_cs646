from transaction import Transaction_info
from block import processed_transaction


def main():
    print("Project 1 by Group 3")
    transaction = Transaction_info()
    block = processed_transaction()

    while True:
        print("--- Menu ---")
        print("1. Add Transaction")
        print("2. Done")
        choice = input("Input # of your choice:")
        if choice == "1":
            file_name = transaction.new_transaction()
            # block.add_transaction(n_t)
            block.process(file_name)

        if choice == "2":
            exit(1)


if __name__ == "__main__":
    main()

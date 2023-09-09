from transaction import Transaction_info
from block2 import processed_transaction


def main():
    print("Project 1 by Group 3")
    t=0
    transaction = Transaction_info()
    block = processed_transaction()
            
    while True:
        print("--- Menu ---")
        print("1. Add Transaction")
        print("2. Done")
        choice = input("Input # of your choice:")

        if choice == "2":
            if t:
                block.process()
            exit(1)
        
        n_t=transaction.new_transaction()
        block.add_transaction(n_t)
        t=1
    


if __name__ == "__main__":
    main()

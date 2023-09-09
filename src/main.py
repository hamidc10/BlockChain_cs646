import os
from transaction import Transaction_info
from block1 import processed_transaction

def main():
    print("Project 1 by Group 3")
    while(True):
        print("--- Menu ---")
        print("1. Add Transaction")
        print("2. Make Block")
        print("3. Exit")
        choice=input("Input # of your choice:")
        
        if(choice=="3"):
            exit(1)
        elif choice=="1":
            transaction=transaction_info
        elif choice=="2":
            block=processed_transaction

if __name__=="__main__":
    main()
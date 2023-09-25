# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 10/1/23

from block import Block
from wallet import Wallet
import os
import shutil

# Driver code
# Updated to test Project 2 requirements with 3 wallets
def main():
    print("Project 2 by Group 3\n")
    print_blocks = input("Enable printing blocks to terminal? (y/n): ")
    block = Block(print_blocks)
    source_pth="../Project2/src/wallet.py"
    Wallet_folder=["Wallet1","Wallet2","Wallet3"]
    for i in Wallet_folder:
        path=os.path.join("../Project2",i)
        if not os.path.exists(path):
            os.mkdir(path)
            shutil.copy(source_pth,path)
            
        
  
    wallet1 = Wallet("Wallet #1")
    wallet2 = Wallet("Wallet #2")
    wallet3 = Wallet("Wallet #3")
    count=0
    
    while True:
        # wallet_lst=os.listdir("../Project2/wallets/")
        print("\n--- Create or Select a wallet ---")
        # print(f"1. {'Create'}")
        # print(f"2. {'View wallets'}")
        print(f"1. {wallet1.name}")
        print(f"2. {wallet2.name}")
        print(f"3. {wallet3.name}")
        choice = input("Input # of your choice: ")
        if choice == "1":
            count+=1
            # wallet=Wallet(input("Please name the wallet: "))
            
            selected_wallet = wallet1
            other_wallets = [wallet2, wallet3]
        elif choice == "2":
            selected_wallet=wallet2
            other_wallets=[wallet1,wallet3]
        else:
            selected_wallet=wallet3
            other_wallets=[wallet1,wallet2]
            
            # if len(wallet_lst)==0:
            #     print("\nThere are no wallets")
            # else:``
            #     print(f"\n Wallets:")
            #     for i in wallet_lst:
            #         print(f"    Wallet owner: {i}")
            # pick=input(f'Please choose a wallet number:')
            # if choice == wallet_lst.index(pick):
            #     print(wallet_lst[int(pick)])

        
        
        print("\n--- Select an action  ---")
        print("1. Create transaction")
        print("2. Check your account balance")
        print("3. Check another account balance")
        choice = input("Input # of your choice: ")
        if choice == "1":
            print("\n--- Select wallet to send to  ---")
            print(f"1. {other_wallets[0].name}")
            print(f"2. {other_wallets[1].name}")
            choice = input("Input # of your choice: ")
            if choice == "1":
                to_address = other_wallets[0].address
            else:
                to_address = other_wallets[1].address
            amount = input("Enter the amount you would like to send: ")
            # Create transaction with wallet
            transaction_file_path = selected_wallet.send(to_address, int(amount))
            # Validate transaction on blockchain
            block.new_block(transaction_file_path)
        elif choice == "2":
            balance = selected_wallet.check_balance()
            print(f"Your account balance ({selected_wallet.name}): {balance}")
        else:
            print("\n--- Select wallet to check balance of ---")
            print(f"1. {other_wallets[0].name}")
            print(f"2. {other_wallets[1].name}")
            choice = input("Input # of your choice: ")
            if choice == "1":
                other_wallet = other_wallets[0]
            else:
                other_wallet = other_wallets[1]
            # Check balance of other wallet using this wallet
            balance = selected_wallet.check_balance(other_wallet.address)
            print(f"Other account balance ({other_wallet.name}): {balance}")


if __name__ == "__main__":
    main()

# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 10/1/23

import os
import shutil
from block import Block
from constants import (
    keys_folder,
    blocks_folder,
    processed_transactions_folder,
    pending_transactions_folder,
    wallet_skeleton,
)
from socket_functions import connect_to_server_socket, send_transaction_file


def init_dirs():
    WM_folder = [("../Node1/WM1","./Wallet1"),("../Node2/WM2","./Wallet2"), ("../Node3/WM3","./Wallet3")]
    # adding the current wallet_skeleton.py to each "Wallet"
    for wm, wallet in WM_folder:
        os.makedirs(wm, exist_ok=True)
        shutil.copy(wallet_skeleton, f"{wm}/wallet.py")
        os.makedirs(wallet, exist_ok=True)
        shutil.copy(wallet_skeleton, f"{wallet}/wallet.py")

    if not os.path.exists(keys_folder):
        os.makedirs(keys_folder,exist_ok=True)

    directories = [
        blocks_folder,
        processed_transactions_folder,
        pending_transactions_folder,
    ]

    # initializing the directories if they don't already exist
    for dir in directories:
        if not os.path.exists(f"../Node1/{dir}"):
            os.makedirs(f"../Node1/{dir}", exist_ok=True)
        if not os.path.exists(f"../Node2/{dir}"):
            os.makedirs(f"../Node2/{dir}", exist_ok=True)
        if not os.path.exists(f"../Node3/{dir}"):
            os.makedirs(f"../Node3/{dir}", exist_ok=True)
        if not os.path.exists(f"../Node4/{dir}"):
            os.makedirs(f"../Node4/{dir}", exist_ok=True)

    main()


def main():
    from Wallet1.wallet import Wallet as W1
    from Wallet2.wallet import Wallet as W2
    from Wallet3.wallet import Wallet as W3


    print("Project 2 by Group 3\n")
    print_blocks = input("Enable printing blocks to terminal? (y/n): ")
    # block = Block(print_blocks)

    wallet1 = W1("Wallet1")
    wallet2 = W2("Wallet2")
    wallet3 = W3("Wallet3")

    while True:
        print("\n--- Select a wallet ---")

        print(f" 1. Wallet 1 address {wallet1.address}")
        print(f" 2. Wallet 2 address {wallet2.address}")
        print(f" 3. Wallet 3 address {wallet3.address}")
        print(" 4. Exit")
        choice = input("\nInput # of your choice: ")

        if choice == "1":
            selected_wallet = wallet1
            other_wallets = [wallet2, wallet3]
        elif choice == "2":
            selected_wallet = wallet2
            other_wallets = [wallet1, wallet3]
        elif choice == "3":
            selected_wallet = wallet3
            other_wallets = [wallet1, wallet2]
        elif choice == "4":
            exit(-1)
        else:
            print("Invalid input try again")
            continue

        print("\n--- Select an action  ---")
        print("1. Create transaction")
        print("2. Check your account balance")
        print("3. Check another account balance")
        choice = input("\nInput # of your choice: ")

        if choice == "1":
            print("\n--- Select wallet to send to  ---")
            print(f"1. {other_wallets[0].name}")
            print(f"2. {other_wallets[1].name}")
            choice = input("\nInput # of your choice: ")
            if choice == "1":
                to_address = other_wallets[0].address
            elif choice == "2":
                to_address = other_wallets[1].address
            else:
                print("Invalid input try again")
                continue
            amount = input("Enter the amount you would like to send: ")

            # Create transaction with wallet
            transaction_name,transaction_file_path = selected_wallet.send(to_address, int(amount))
            server=connect_to_server_socket()
            send_transaction_file(server,transaction_name, transaction_file_path)
            # miner.new_block(transaction_file_path)

        elif choice == "2":
            balance = selected_wallet.check_balance()
            print(f"Your account balance ({selected_wallet.name}): {balance}")

        elif choice == "3":
            print("\n--- Select wallet to check balance of ---")
            print(f"1. {other_wallets[0].name}")
            print(f"2. {other_wallets[1].name}")
            choice = input("\nInput # of your choice: ")
            
            if choice == "1":
                other_wallet = other_wallets[0]
            else:
                other_wallet = other_wallets[1]

            # Check balance of other wallet using this wallet
            balance = selected_wallet.check_balance(other_wallet.address)
            print(f"Other account balance ({other_wallet.name}): {balance}")
        else:
            print("Invalid input try again")
            continue


if __name__ == "__main__":
    init_dirs()

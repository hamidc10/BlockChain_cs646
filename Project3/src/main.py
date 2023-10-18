# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 10/1/23

import os
import shutil
import threading
from block import Block
from constants import (
    keys_folder,
    blocks_folder,
    processed_transactions_folder,
    pending_transactions_folder,
    wallet_skeleton,
    client_skeleton
)

ports = [1001, 1002, 1003]
def init_nodes():
    Nodes_folder = ["Node1", "Node2", "Node3"]
    Wallet_folder = ["Wallet1", "Wallet2", "Wallet3"]
    
    for node, wallet in zip(Nodes_folder, Wallet_folder):
        # Create the Node folder
        os.makedirs(node, exist_ok=True)
        os.makedirs(os.path.join(node, wallet), exist_ok=True)
        shutil.copy(client_skeleton, f"{node}/client.py")
        shutil.copy(wallet_skeleton, os.path.join(node, wallet, "wallet.py"))
        
        directories = [
            keys_folder,
            blocks_folder,
            processed_transactions_folder,
            pending_transactions_folder,
        ]
        
        for dir in directories:
            if not os.path.exists(f"{node}/{dir}"):
                os.makedirs(os.path.join(node, dir), exist_ok=True)

    main(ports)

def client_start(node_folder, port):
    node_c = f"{node_folder}.client"
    client = __import__(node_c, fromlist=['Client'])
    client_call = client.Client(port)
    client_call.run()


# def init_dirs():
#     Wallet_folder = ["Wallet1", "Wallet2", "Wallet3"]
#     # adding the current wallet_skeleton.py to each "Wallet"
#     for wallet in Wallet_folder:
#         os.makedirs(wallet, exist_ok=True)
#         shutil.copy(wallet_skeleton, f"{wallet}/wallet.py")

#     directories = [
#         keys_folder,
#         blocks_folder,
#         processed_transactions_folder,
#         pending_transactions_folder,
#     ]

#     # initializing the directories if they don't already exist
#     for dir in directories:
#         if not os.path.exists(dir):
#             os.makedirs(dir, exist_ok=True)
    


def main(ports):
    from Node1.Wallet1.wallet import Wallet as W1
    from Node2.Wallet2.wallet import Wallet as W2
    from Node3.Wallet3.wallet import Wallet as W3

    threads = []
    for i, node_folder in enumerate(["Node1", "Node2", "Node3"]):
        t = threading.Thread(target=client_start, args=(node_folder, ports[i]))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    print("Project 2 by Group 3\n")
    print_blocks = input("Enable printing blocks to terminal? (y/n): ")
    block = Block(print_blocks)

    wallet1 = W1("Node1","Wallet1")
    wallet2 = W2("Node2","Wallet2")
    wallet3 = W3("Node3","Wallet3")

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
            transaction_file_path = selected_wallet.send(to_address, int(amount))
            block.new_block(transaction_file_path)

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
    init_nodes()
    
    # init_dirs()

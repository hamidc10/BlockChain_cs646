# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 10/22/23

import os
import time
import random

from src.wallet import Wallet
from src.constants import pending_transactions_folder


# Driver code
def main():
    print("Project 4 by Group 3\n")
    wallet1 = Wallet("Wallet A")
    wallet2 = Wallet("Wallet B")
    wallet3 = Wallet("Wallet C")

    print("Starting test simulation...")
    print(
        "You will be able to test different features with multiple wallets interacting on the blockchain"
    )
    print("To exit the loop, kill the program (CTRL+C)")

    while True:
        print("\n--- Select your wallet ---")
        print(f"1. {wallet1.name} (balance: {wallet1.check_balance()})")
        print(f"2. {wallet2.name} (balance: {wallet2.check_balance()})")
        print(f"3. {wallet3.name} (balance: {wallet3.check_balance()})")
        choice = input("Input # of your choice: ")
        if choice == "1":
            selected_wallet = wallet1
            other_wallets = [wallet2, wallet3]
        elif choice == "2":
            selected_wallet = wallet2
            other_wallets = [wallet1, wallet3]
        else:
            selected_wallet = wallet3
            other_wallets = [wallet1, wallet2]

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
            # Pick random node to validate transaction on blockchain
            node_folder = random.choice(["node1", "node2", "node3"])
            print(f"Randomly picked {node_folder} to process transaction")
            transactions_folder = os.path.join(node_folder, pending_transactions_folder)
            # Create transaction with wallet
            selected_wallet.send(to_address, int(amount), transactions_folder)
            # Give some time for node to process transaction
            print("Waiting 3 seconds for node to process transaction before moving on")
            time.sleep(3)
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

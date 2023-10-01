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


def init_dirs():
    Wallet_folder = ["Wallet1", "Wallet2", "Wallet3"]
    for wallet in Wallet_folder:
        # adding the current wallet_skeleton.py to the wallet
        os.makedirs(wallet, exist_ok=True)
        shutil.copy(wallet_skeleton, f"{wallet}/wallet.py")

        # path_py = os.path.join(wallet, "__init__.py")
        # if not os.path.exists(path_py):
        #     with open(path_py, "w") as f:
        #         pass

    directories = [
        keys_folder,
        blocks_folder,
        processed_transactions_folder,
        pending_transactions_folder,
    ]

    # initializing the directories if they don't already exist
    for dir in directories:
        if not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)

    main()


def main():
    from Wallet1.wallet import Wallet as W1
    from Wallet2.wallet import Wallet as W2
    from Wallet3.wallet import Wallet as W3

    print("Project 2 by Group 3\n")
    print_blocks = input("Enable printing blocks to terminal? (y/n): ")
    block = Block(print_blocks)

    wallet1 = W1("Wallet1")
    wallet2 = W2("Wallet2")
    wallet3 = W3("Wallet3")

    while True:
        print("\n--- Select a wallet ---")

        print(f" 1. Wallet 1 address {wallet1.address}")
        print(f" 2. Wallet 2 address {wallet2.address}")
        print(f" 3. Wallet 3 address {wallet3.address}")
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

            # Create transaction with wallet
            transaction_file_path = selected_wallet.send(to_address, int(amount))
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
    init_dirs()

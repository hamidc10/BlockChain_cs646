# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 10/1/23

from block import Block
# from wallet import Wallet
import os
import shutil
import rsa
import sys

source_pth="wallet.py"
temp_path=""


Wallet_folder=["Wallet1","Wallet2","Wallet3"]
for i in Wallet_folder:
    path = os.path.abspath(os.path.join(temp_path, i))
    public_key,private_key=rsa.newkeys(2048)
    
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        shutil.copy(source_pth,path)
        with open(path+"/public.pem", "wb+") as f:
            f.write(public_key.save_pkcs1("PEM"))
        with open(path+"/private.pem", "wb+") as f:
            f.write(private_key.save_pkcs1("PEM"))

W1_path_pb=os.path.join(temp_path,Wallet_folder[0],"/public.pem")
W2_path_pb=os.path.join(temp_path,Wallet_folder[1],"/public.pem")
W3_path_pb=os.path.join(temp_path,Wallet_folder[2],"/public.pem")

W1_path_pv=os.path.join(temp_path,Wallet_folder[0],"/private.pem")
W2_path_pv=os.path.join(temp_path,Wallet_folder[1],"/private.pem")
W3_path_pv=os.path.join(temp_path,Wallet_folder[2],"/private.pem")

W1_path_py=os.path.join(temp_path,Wallet_folder[0],"/__init__.py")
W2_path_py=os.path.join(temp_path,Wallet_folder[1],"/__init__.py")
W3_path_py=os.path.join(temp_path,Wallet_folder[2],"/__init__.py")

if not os.path.exists(W1_path_pb) or  not os.path.exists(W1_path_pv) or not os.path.exists(W1_path_py):
    with open("Wallet1/public.pem", "wb+") as f:
        f.write(public_key.save_pkcs1("PEM"))
    with open("Wallet1/private.pem", "wb+") as f:
        f.write(private_key.save_pkcs1("PEM"))
    with open("Wallet1/__init__.py","w") as f:
        pass
        
if not os.path.exists(W2_path_pb) or not os.path.exists(W2_path_pv) or not os.path.exists(W2_path_py):
    with open("Wallet2/public.pem", "wb+") as f:
        f.write(public_key.save_pkcs1("PEM"))
    with open("Wallet2/private.pem", "wb+") as f:
        f.write(private_key.save_pkcs1("PEM"))
    with open("Wallet2/__init__.py","w") as f:
        pass

if not os.path.exists(W3_path_pb) or not os.path.exists(W3_path_pv) or not os.path.exists(W3_path_py):
    with open("Wallet3/public.pem", "wb+") as f:
        f.write(public_key.save_pkcs1("PEM"))
    with open("Wallet3/private.pem", "wb+") as f:
        f.write(private_key.save_pkcs1("PEM"))
    with open("Wallet3/__init__.py","w") as f:
        pass


from Wallet1.wallet import Wallet as W1
from Wallet2.wallet import Wallet as W2
from Wallet3.wallet import Wallet as W3


def main():
    print("Project 2 by Group 3\n")
    print_blocks = input("Enable printing blocks to terminal? (y/n): ")
    block = Block(print_blocks)
            
        
  
    wallet1 = W1("Wallet1")
    wallet2 = W2("Wallet2")
    wallet3 = W3("Wallet3")
   
    
    while True:
       
        print("\n--- Create or Select a wallet ---")
        print(f"1. {'Create'}")
        print(f"2. {'View wallets'}")
        print(f"1. {wallet1.address}")
        print(f"2. {wallet2.address}")
        print(f"3. {wallet3.address}")
        choice = input("Input # of your choice: ")
        # if choice == "1":
        #     count+=1
        #     # wallet=Wallet(input("Please name the wallet: "))
            
        #     selected_wallet = wallet1
        #     other_wallets = [wallet2, wallet3]
        # elif choice == "2":
        #     selected_wallet=wallet2
        #     other_wallets=[wallet1,wallet3]
        # else:
        #     selected_wallet=wallet3
        #     other_wallets=[wallet1,wallet2]
            
        #     # if len(wallet_lst)==0:
        #     #     print("\nThere are no wallets")
        #     # else:``
        #     #     print(f"\n Wallets:")
        #     #     for i in wallet_lst:
        #     #         print(f"    Wallet owner: {i}")
        #     # pick=input(f'Please choose a wallet number:')
        #     # if choice == wallet_lst.index(pick):
        #     #     print(wallet_lst[int(pick)])

        
        
        # print("\n--- Select an action  ---")
        # print("1. Create transaction")
        # print("2. Check your account balance")
        # print("3. Check another account balance")
        # choice = input("Input # of your choice: ")
        # if choice == "1":
        #     print("\n--- Select wallet to send to  ---")
        #     print(f"1. {other_wallets[0].name}")
        #     print(f"2. {other_wallets[1].name}")
        #     choice = input("Input # of your choice: ")
        #     if choice == "1":
        #         to_address = other_wallets[0].address
        #     else:
        #         to_address = other_wallets[1].address
        #     amount = input("Enter the amount you would like to send: ")
        #     # Create transaction with wallet
        #     transaction_file_path = selected_wallet.send(to_address, int(amount))
        #     # Validate transaction on blockchain
        #     block.new_block(transaction_file_path)
        # elif choice == "2":
        #     balance = selected_wallet.check_balance()
        #     print(f"Your account balance ({selected_wallet.name}): {balance}")
        # else:
        #     print("\n--- Select wallet to check balance of ---")
        #     print(f"1. {other_wallets[0].name}")
        #     print(f"2. {other_wallets[1].name}")
        #     choice = input("Input # of your choice: ")
        #     if choice == "1":
        #         other_wallet = other_wallets[0]
        #     else:
        #         other_wallet = other_wallets[1]
        #     # Check balance of other wallet using this wallet
        #     balance = selected_wallet.check_balance(other_wallet.address)
        #     print(f"Other account balance ({other_wallet.name}): {balance}")


if __name__ == "__main__":
    main()

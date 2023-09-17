# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 10/1/23

import json
from typing import Dict

from constants import account_state_file_path

# map of user addresses to balances
AccountStateDict = Dict[str, int]


# TODO: use this in block.py and wallet.py
def load_account_state() -> AccountStateDict:
    with open(account_state_file_path, "r") as f:
        return json.load(f)


# TODO: use this in block.py
def save_account_state(state: AccountStateDict):
    with open(account_state_file_path, "w") as f:
        json.dump(state, f)


# TODO: use this in block.py
def init_account_state():
    save_account_state({})

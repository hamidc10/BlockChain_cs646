# We (Hamid, Chantel, Vira, Trey, Xavier) declare that we have completed this computer code in accordance with the UAB Academic Integrity Code and the UAB CS Honor Code.
# We have read the UAB Academic Integrity Code and understand that any breach of the Code may result in severe penalties.
# Student initials: HC, CRW, VVS, TC, XM
# Date: 10/22/23

import os
import time
import json
from typing import Dict

from src.constants import (
    account_state_file_path,
    account_state_lock_path,
    default_wallet_balance,
)

# map of user addresses to balances
# AccountStateDict[address] = balance
AccountStateDict = Dict[str, int]


def account_state_is_locked() -> bool:
    return os.path.exists(account_state_lock_path)


def lock_account_state():
    with open(account_state_lock_path, "w") as f:
        f.write("lock")


def unlock_account_state():
    if account_state_is_locked():
        os.remove(account_state_lock_path)


def load_account_state() -> AccountStateDict:
    # load current account state
    if os.path.exists(account_state_file_path):
        with open(account_state_file_path, "r") as f:
            return json.load(f)
    # file does not exist yet
    return {}


def update_account_state(transaction: dict):
    # wait for any current updates to be finished
    while account_state_is_locked():
        time.sleep(0.2)

    # create lock file to prevent conflicting updates
    lock_account_state()

    # load current account state
    account_state = load_account_state()

    # update account state
    amount = transaction["Amount"]
    from_address = transaction["From"]
    to_address = transaction["To"]
    account_state[from_address] = (
        account_state.get(from_address, default_wallet_balance) - amount
    )
    account_state[to_address] = (
        account_state.get(to_address, default_wallet_balance) + amount
    )

    # save account state
    with open(account_state_file_path, "w+") as f:
        json.dump(account_state, f)

    # unlock account state
    unlock_account_state()

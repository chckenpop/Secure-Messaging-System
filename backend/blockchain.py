# from web3 import Web3
# import json

# RPC_URL = "http://127.0.0.1:8545"
# CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

# ABI_PATH = "../blockchain/artifacts/contracts/SecureMessaging.sol/SecureMessaging.json"

# with open(ABI_PATH) as f:
#     contract_json = json.load(f)
#     CONTRACT_ABI = contract_json["abi"]

# w3 = Web3(Web3.HTTPProvider(RPC_URL))

# def get_contract():
#     if not w3.is_connected():
#         return None
    
#     w3.eth.default_account = w3.eth.accounts[0]
    
#     return w3.eth.contract(
#         address=CONTRACT_ADDRESS,
#         abi=CONTRACT_ABI
#     )

# def get_message_count():
#     contract = get_contract()
#     if contract is None:
#         return "Blockchain not connected"
    
#     return contract.functions.getMessageCount().call()

from web3 import Web3
import json
import os

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

with open("../blockchain/artifacts/contracts/SecureMessaging.sol/SecureMessaging.json") as f:
    contract_json = json.load(f)
    contract_abi = contract_json["abi"]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)


HARDHAT_PRIVATE_KEYS = [
    "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80",
    "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d",
    "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a",
    "0x7c852118294e51e653712a81e05800f419141751be58f605c371e15141b007a6"
]

account_index = 0

def create_eth_account():
    global account_index

    private_key = HARDHAT_PRIVATE_KEYS[account_index]
    account = w3.eth.account.from_key(private_key)

    account_index += 1

    return account.address, private_key


def register_user_on_chain(eth_private_key, public_key):
    account = w3.eth.account.from_key(eth_private_key)

    nonce = w3.eth.get_transaction_count(account.address)

    tx = contract.functions.registerUser(public_key).build_transaction({
        "from": account.address,
        "nonce": nonce,
        "gas": 2000000,
        "gasPrice": w3.to_wei("1", "gwei")
    })

    signed_tx = w3.eth.account.sign_transaction(tx, eth_private_key)

    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    w3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_hash.hex()


def log_message_on_chain(sender_private_key, receiver_address, message_hash):
    account = w3.eth.account.from_key(sender_private_key)
    nonce = w3.eth.get_transaction_count(account.address)

    tx = contract.functions.logMessage(receiver_address, message_hash).build_transaction({
        "from": account.address,
        "nonce": nonce,
        "gas": 2000000,
        "gasPrice": w3.to_wei("1", "gwei")
    })

    signed_tx = w3.eth.account.sign_transaction(tx, sender_private_key)
    tx_hash = tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)


    w3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_hash.hex()


def get_contract():
    if not w3.is_connected():
        return None
    
    w3.eth.default_account = w3.eth.accounts[0]
    
    return w3.eth.contract(
        address=CONTRACT_ADDRESS,
        abi=CONTRACT_ABI
    )

def get_message_count():
    contract = get_contract()
    if contract is None:
        return "Blockchain not connected"
    
    return contract.functions.getMessageCount().call()


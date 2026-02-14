from fastapi import FastAPI
from crypto_utils import generate_rsa_keys, encrypt_message, decrypt_message, hash_payload
from database import store_message, get_message
from blockchain import get_message_count
from blockchain import create_eth_account, register_user_on_chain, log_message_on_chain
from models.message_models import SendMessageRequest, ReceiveMessageRequest
import uuid
from blockchain import get_message_hash
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary in-memory user store (for demo)
users = {}

@app.get("/")
def root():
    return {"status": "Backend running"}

@app.post("/register-user")
def register_user():
    private_key, public_key = generate_rsa_keys()

    eth_address, eth_private_key = create_eth_account()

    tx_hash = register_user_on_chain(eth_private_key, public_key)

    user_id = str(uuid.uuid4())

    users[user_id] = {
        "private_key": private_key,
        "public_key": public_key,
        "eth_address": eth_address,
        "eth_private_key": eth_private_key
    }

    return {
        "user_id": user_id,
        "eth_address": eth_address,
        "blockchain_tx": tx_hash
    }

@app.post("/send-message")
def send_message(request: SendMessageRequest):
    sender_id = request.sender_id
    receiver_id = request.receiver_id
    message = request.message

    sender = users.get(sender_id)
    receiver = users.get(receiver_id)

    if not sender:
        return {"error": "Sender not found"}

    if not receiver:
        return {"error": "Receiver not found"}

    encrypted = encrypt_message(message, receiver["public_key"])
    message_hash = hash_payload(encrypted)

    tx_hash = log_message_on_chain(
        sender["eth_private_key"],
        receiver["eth_address"],
        message_hash
    )

    message_id = store_message({
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "payload": encrypted,
        "hash": message_hash
    })

    return {
        "message_id": message_id,
        "hash": message_hash,
        "blockchain_tx": tx_hash
    }


@app.post("/receive-message")
def receive_message(request: ReceiveMessageRequest):
    user_id = request.user_id
    message_id = request.message_id
    message_data = get_message(message_id)

    if not message_data:
        return {"error": "Message not found"}

    payload = message_data["payload"]
    stored_hash = message_data["hash"]

    calculated_hash = hash_payload(payload)

    if stored_hash != calculated_hash:
        return {"error": "Message integrity compromised"}

    user = users.get(user_id)
    if not user:
        return {"error": "User not found"}

    private_key = user["private_key"]

    decrypted = decrypt_message(payload, private_key)

    return {
        "decrypted_message": decrypted,
        "integrity_verified": True
    }



@app.get("/verify-on-chain/{index}")
def verify_on_chain(index: int):
    on_chain_hash = get_message_hash(index)
    return {
        "on_chain_hash": on_chain_hash
    }

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64
import hashlib

# Generate RSA key pair
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return private_pem.decode(), public_pem.decode()


# AES encryption
def encrypt_message(message: str, public_key_pem: str):
    # Generate AES key
    aes_key = os.urandom(32)

    # Generate IV
    iv = os.urandom(16)

    cipher = Cipher(
        algorithms.AES(aes_key),
        modes.CFB(iv),
        backend=default_backend()
    )

    encryptor = cipher.encryptor()
    encrypted_message = encryptor.update(message.encode()) + encryptor.finalize()

    # Encrypt AES key with RSA
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode()
    )

    encrypted_aes_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return {
        "encrypted_message": base64.b64encode(encrypted_message).decode(),
        "encrypted_aes_key": base64.b64encode(encrypted_aes_key).decode(),
        "iv": base64.b64encode(iv).decode()
    }


# AES decryption
def decrypt_message(encrypted_data: dict, private_key_pem: str):
    encrypted_message = base64.b64decode(encrypted_data["encrypted_message"])
    encrypted_aes_key = base64.b64decode(encrypted_data["encrypted_aes_key"])
    iv = base64.b64decode(encrypted_data["iv"])

    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(),
        password=None
    )

    aes_key = private_key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    cipher = Cipher(
        algorithms.AES(aes_key),
        modes.CFB(iv),
        backend=default_backend()
    )

    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()

    return decrypted_message.decode()


def hash_payload(payload: dict):
    combined = payload["encrypted_message"] + payload["encrypted_aes_key"] + payload["iv"]
    return hashlib.sha256(combined.encode()).hexdigest()

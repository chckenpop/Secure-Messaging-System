# 🔐 Blockchain-Based Secure Messaging System

A modular secure messaging system that combines end-to-end encryption with blockchain-based integrity verification.

This project demonstrates practical integration of:

- Smart contracts (Solidity)
- Local Ethereum blockchain (Hardhat)
- Python backend (FastAPI)
- Cryptographic security (AES + RSA)
- Off-chain encrypted storage

---

## 🚀 Key Features

- 🔑 Public key registration on blockchain  
- 🔐 Hybrid encryption (AES for data, RSA for key exchange)  
- 🧾 Tamper-proof message hash logging on-chain  
- 📦 Encrypted message storage off-chain (scalable design)  
- 🧠 Clean separation between blockchain and backend layers  

---

## 🏗 System Architecture

User
↓
Encrypt (AES)
↓
FastAPI Backend
↓
MongoDB (Encrypted Storage)
↓
SHA-256 Hash
↓
Ethereum Smart Contract


### Design Principles

- Blockchain used for trust anchoring, not storage
- Encrypted messages stored off-chain for scalability
- Hash-based integrity verification
- Modular backend architecture for future extensibility

---

## 🔒 Security Model

| Property | Implementation |
|----------|---------------|
| Confidentiality | AES + RSA hybrid encryption |
| Integrity | SHA-256 hash stored on blockchain |
| Authenticity | Ethereum transaction identity |
| Non-repudiation | Immutable blockchain log |
| Scalability | Off-chain encrypted storage |

---

## 🛠 Tech Stack

### Blockchain
- Solidity
- Hardhat
- Ethers.js

### Backend
- FastAPI
- Web3.py
- MongoDB
- Python `cryptography` library

---

## 🧪 Local Development

### 1️⃣ Start Local Blockchain

```bash
cd blockchain
npx hardhat node

### 2️⃣ Deploy Smart Contract

npx hardhat run scripts/deploy.js --network localhost

 ### 3️⃣ Run Backend
 cd backend
uvicorn main:app --reload

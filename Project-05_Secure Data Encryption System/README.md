# 🔐 Secure Data Encryption System

A simple Streamlit app that allows users to securely **encrypt and store** data using custom passkeys and **retrieve it** using the correct credentials.

## 💡 Features
- Encrypt and store data with a passkey
- Decrypt data using a unique Data ID and passkey
- Hashing and encryption using `cryptography` & `hashlib`
- Anti-brute-force mechanism with login reauthorization
- Fully in-memory (no database)

## 🛠️ Technologies
- Python
- Streamlit
- cryptography (Fernet)
- hashlib & base64

## 📦 Setup Instructions
```bash
git clone https://github.com/yourusername/secure-encryption-app.git
cd secure-encryption-app
pip install -r requirements.txt
streamlit run app.py
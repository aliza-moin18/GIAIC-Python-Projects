import streamlit as st
import hashlib
import json
import time
from cryptography.fernet import Fernet
import base64
import uuid

# ======================= SESSION VARIABLES =======================
if 'failed_attempts' not in st.session_state:
    st.session_state.failed_attempts = 0
if 'stored_data' not in st.session_state:
    st.session_state.stored_data = {}
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'last_attempt_time' not in st.session_state:
    st.session_state.last_attempt_time = 0


# ======================= UTILITY FUNCTIONS =======================

def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

def generate_key_from_passkey(passkey):
    hashed = hashlib.sha256(passkey.encode()).digest()
    return base64.urlsafe_b64encode(hashed[:32])

def encrypt_data(text, passkey):
    key = generate_key_from_passkey(passkey)
    cipher = Fernet(key)
    return cipher.encrypt(text.encode()).decode()

def decrypt_data(encrypted_text, passkey, data_id):
    try:
        hashed_passkey = hash_passkey(passkey)
        if data_id in st.session_state.stored_data and st.session_state.stored_data[data_id]["passkey"] == hashed_passkey:
            key = generate_key_from_passkey(passkey)
            cipher = Fernet(key)
            decrypted = cipher.decrypt(encrypted_text.encode()).decode()
            st.session_state.failed_attempts = 0
            return decrypted
        else:
            st.session_state.failed_attempts += 1
            st.session_state.last_attempt_time = time.time()
            return None
    except Exception:
        st.session_state.failed_attempts += 1
        st.session_state.last_attempt_time = time.time()
        return None

def generate_data_id():
    return str(uuid.uuid4())

def reset_failed_attempts():
    st.session_state.failed_attempts = 0

def change_page(page):
    st.session_state.current_page = page


# ======================= MAIN INTERFACE =======================

st.title("🔐 Secure Data Encryption App")

# Navigation Menu
menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("📁 Menu", menu, index=menu.index(st.session_state.current_page))
st.session_state.current_page = choice

# Auto-lock after 3 failed attempts
if st.session_state.failed_attempts >= 3:
    st.session_state.current_page = "Login"
    st.warning("Too many failed attempts. Please reauthorize.")


# ======================= HOME SECTION =======================

if st.session_state.current_page == "Home":
    st.subheader("Welcome")
    st.write("Securely store and retrieve encrypted data using a custom passkey.")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Store New Data", use_container_width=True):
            change_page("Store Data")
    with col2:
        if st.button("🔓 Retrieve Data", use_container_width=True):
            change_page("Retrieve Data")
    
    st.info(f"Total entries stored: {len(st.session_state.stored_data)}")


# ======================= STORE DATA SECTION =======================

elif st.session_state.current_page == "Store Data":
    st.subheader("🔒 Store Data")
    user_data = st.text_area("Enter your data:")
    passkey = st.text_input("Set a passkey:", type="password")
    confirm_passkey = st.text_input("Confirm passkey:", type="password")

    if st.button("Encrypt & Save"):
        if user_data and passkey and confirm_passkey:
            if passkey != confirm_passkey:
                st.error("Passkeys do not match.")
            else:
                data_id = generate_data_id()
                hashed_passkey = hash_passkey(passkey)
                encrypted_text = encrypt_data(user_data, passkey)
                st.session_state.stored_data[data_id] = {
                    "encrypted_text": encrypted_text,
                    "passkey": hashed_passkey
                }
                st.success("Data encrypted and stored successfully.")
                st.code(data_id, language="text")
                st.info("Save this Data ID to retrieve your data later.")
        else:
            st.warning("All fields are required.")


# ======================= RETRIEVE DATA SECTION =======================

elif st.session_state.current_page == "Retrieve Data":
    st.subheader("🔍 Retrieve Data")
    attempts_remaining = 3 - st.session_state.failed_attempts
    st.info(f"Attempts remaining: {attempts_remaining}")
    
    data_id = st.text_input("Enter your Data ID:")
    passkey = st.text_input("Enter your Passkey:", type="password")

    if st.button("Decrypt"):
        if data_id and passkey:
            if data_id in st.session_state.stored_data:
                encrypted_text = st.session_state.stored_data[data_id]["encrypted_text"]
                decrypted_text = decrypt_data(encrypted_text, passkey, data_id)
                if decrypted_text:
                    st.success("Decryption successful.")
                    st.markdown("### Decrypted Data:")
                    st.code(decrypted_text, language="text")
                else:
                    st.error(f"Incorrect passkey. {3 - st.session_state.failed_attempts} attempts left.")
            else:
                st.error("Invalid Data ID.")
            if st.session_state.failed_attempts >= 3:
                st.warning("Too many failed attempts. Redirecting to login.")
                st.session_state.current_page = "Login"
                st.rerun()
        else:
            st.warning("Please fill all fields.")


# ======================= LOGIN SECTION =======================

elif st.session_state.current_page == "Login":
    st.subheader("🔑 Reauthorization")

    time_elapsed = time.time() - st.session_state.last_attempt_time
    wait_time = 10

    if st.session_state.failed_attempts >= 3 and time_elapsed < wait_time:
        remaining_time = int(wait_time - time_elapsed)
        with st.empty():
            st.warning(f"⏳ Please wait {remaining_time} seconds before retrying.")
            time.sleep(1)
            st.rerun()
    else:
        login_pass = st.text_input("Enter Admin Password:", type="password")
        if st.button("Login"):
            if login_pass == "admin123":
                reset_failed_attempts()
                st.success("✅ Access granted.")
                st.session_state.current_page = "Home"
                st.rerun()
            else:
                st.error("❌ Incorrect password.")


# ======================= FOOTER =======================

st.markdown("---")
st.markdown("Developed by **Aliza Moin** ")
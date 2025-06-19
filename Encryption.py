from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import bcrypt

load_dotenv()

def get_key_from_env():
    key = os.getenv("FERNET_KEY")
    if not key:
        raise ValueError("FERNET_KEY not found in environment. Please generate it first.")
    return key

def encrypt_data(message):
    key = get_key_from_env()
    cipher = Fernet(key)
    token = cipher.encrypt(message.encode())
    return token

def decrypt_data(token):
    key = get_key_from_env()
    cipher = Fernet(key)
    decrypted = cipher.decrypt(token)
    return decrypted.decode()

def hash_password(password):
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed

def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode(), hashed_password)

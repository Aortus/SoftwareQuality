from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import sqlite3

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

import sqlite3

def get_all_admins():
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins")
    admins = cursor.fetchall()
    conn.close()

    decrypted_admins = []
    for admin in admins:
        admin_list = list(admin)  # convert tuple to list so we can modify it
        admin_list[1] = decrypt_data(admin_list[1])  # decrypt username
        decrypted_admins.append(tuple(admin_list))

    return decrypted_admins


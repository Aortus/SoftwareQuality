import sqlite3
import bcrypt
import re
import Encryption
import LoginUI
import Login
import datetime
import ManageTraveller
import ManageAdmin
import Logs
import Backup


# === Setup database ===
# def SetupDB():
#     conn = sqlite3.connect("SQDB.db")
#     cursor = conn.cursor()
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS admins (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         username TEXT,
#         password_hash TEXT,
#         firstname TEXT,
#         lastname TEXT,
#         registration_date TEXT,
#         admin_type TEXT
#     )
#     """)
#     conn.commit()
#     cursor = conn.cursor()

#     hashed = bcrypt.hashpw("Admin_123?".encode(), bcrypt.gensalt())
#     enc_username = Encryption.encrypt_data("super_admin")
#     enc_firstname = Encryption.encrypt_data("Super")
#     enc_lastname = Encryption.encrypt_data("Admin")
#     enc_admintype = Encryption.encrypt_data("Super Administrator")
#     enc_date = Encryption.encrypt_data(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     try:
#         cursor.execute("INSERT INTO admins (username, password_hash, firstname, lastname, registration_date, admin_type) VALUES (?, ?, ?, ?, ?, ?)", (enc_username, hashed, enc_firstname, enc_lastname, enc_date, enc_admintype))
#     except sqlite3.IntegrityError:
#         print("Admin user already exists.")
#     conn.commit()
#     conn.close()
#     conn = sqlite3.connect("SQDB.db")
#     cursor = conn.cursor()

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
#         firstname TEXT,
#         lastname TEXT,
#         birthdate DATE,
#         gender TEXT,
#         streetname TEXT,
#         streetnumber TEXT,
#         zipcode TEXT,
#         city TEXT,
#         email TEXT UNIQUE,
#         mobilephone TEXT,
#         drivinglicense TEXT
#     )
#     """)
#     # To do: make the user ID in another way               
#     conn.commit()
#     conn.close()

    # conn = sqlite3.connect("SQDB.db")
    # cursor = conn.cursor()

    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS scooters (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     brand TEXT,
    #     model TEXT,
    #     serialnumber TEXT UNIQUE,
    #     topspeed INTEGER,
    #     batterycapacity INTEGER,
    #     stateofcharge INTEGER,
    #     targetstateofcharge INTEGER,
    #     location TEXT,
    #     outofservice BOOLEAN,
    #     mileage INTEGER,
    #     lastmaintenance DATETIME,
    #     inservicedate DATETIME DEFAULT CURRENT_TIMESTAMP
    # )
    # """
    # )    
    # conn.commit()
    # conn.close()

    # cursor = conn.cursor()         
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS logs (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    #     user_id INTEGER,
    #     action TEXT,
    #     details TEXT,
    #     is_suspicious INTEGER DEFAULT 0,
    #     is_read INTEGER DEFAULT 0
    # )
    # """
    # )
    # conn.commit()
    # conn.close()

    
if __name__ == "__main__":
    # SetupDB()
    LoginUI.login_screen()

    # Admin Login: super_admin / Admin_123?
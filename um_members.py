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
#def SetupDB():
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

    # cursor.execute("DROP TABLE IF EXISTS scooters")

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
    #     lastmaintenance DATETIME
    # )
    # """
    # )     
    # conn.commit()
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
    # conn = sqlite3.connect("SQDB.db")
    # cursor = conn.cursor()
    # enc_username2 = Encryption.encrypt_data("service_engineer")
    # enc_firstname2 = Encryption.encrypt_data("service")
    # enc_lastname2 = Encryption.encrypt_data("engineer")
    # enc_admintype2 = Encryption.encrypt_data("Service Engineer")
    # enc_date2 = Encryption.encrypt_data(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # hashed2 = bcrypt.hashpw("ServiceEng".encode(), bcrypt.gensalt())
    # try:
    #     cursor.execute("INSERT INTO admins (username, password_hash, firstname, lastname, registration_date, admin_type) VALUES (?, ?, ?, ?, ?, ?)", (enc_username2, hashed2, enc_firstname2, enc_lastname2, enc_date2, enc_admintype2))
    #     print("Service Engineer user created successfully.")
    # except sqlite3.IntegrityError:
    #     print("Service Engineer user already exists.")
    # conn.commit()
    # conn.close()


    # conn = sqlite3.connect("SQDB.db")
    # cursor = conn.cursor()
    # enc_brand = Encryption.encrypt_data("Xiaomi")
    # enc_model = Encryption.encrypt_data("M365")
    # enc_serialnumber = Encryption.encrypt_data("XIA1234567890")
    # enc_topspeed = Encryption.encrypt_data("25")
    # enc_batterycapacity = Encryption.encrypt_data("5000")
    # enc_stateofcharge = Encryption.encrypt_data("100")
    # enc_targetstateofcharge = Encryption.encrypt_data("100")
    # enc_location = Encryption.encrypt_data("51.9225, 4.47917")  # Example coordinates in Rotterdam
    # enc_outofservice = Encryption.encrypt_data("0")
    # enc_mileage = Encryption.encrypt_data("0")
    # enc_lastmaintenance = Encryption.encrypt_data(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    # try:
    #     cursor.execute("INSERT INTO scooters (brand, model, serialnumber, topspeed, batterycapacity, stateofcharge, targetstateofcharge, location, outofservice, mileage, lastmaintenance) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
    #                    (enc_brand, enc_model, enc_serialnumber, enc_topspeed, enc_batterycapacity, enc_stateofcharge, enc_targetstateofcharge, enc_location, enc_outofservice, enc_mileage, enc_lastmaintenance))
    #     print("Scooter created successfully.")
    # except sqlite3.IntegrityError:
    #     print("Scooter already exists.")
    # conn.commit()
    # conn.close()

    # conn = sqlite3.connect("SQDB.db")
    # cursor = conn.cursor()
    # enc_username2 = Encryption.encrypt_data("system_admin")
    # enc_firstname2 = Encryption.encrypt_data("system")
    # enc_lastname2 = Encryption.encrypt_data("admin")
    # enc_admintype2 = Encryption.encrypt_data("System Administrator")
    # hashed2 = bcrypt.hashpw("SystemAd".encode(), bcrypt.gensalt())
    # enc_registration_date2 = Encryption.encrypt_data(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # try:
    #     cursor.execute("INSERT INTO admins (username, password_hash, firstname, lastname, registration_date, admin_type) VALUES (?, ?, ?, ?, ?, ?)", 
    #                    (enc_username2, hashed2, enc_firstname2, enc_lastname2, enc_registration_date2, enc_admintype2))
    #     print("System Admin user created successfully.")
    # except sqlite3.IntegrityError:
    #     print("System Admin user already exists.")

    # conn.commit()
    # conn.close()

    
if __name__ == "__main__":
    #SetupDB()
    LoginUI.login_screen()

    # ServiceEngineer Login: service_engineer / ServiceEng    ???????? Service_Engineer123?
    # Admin Login: super_admin / Admin_123?
    # SystemAdmin Login: system_admin / SystemAd
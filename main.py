import sqlite3
import bcrypt
import re
import Login


# === Setup database ===
def SetupDB():
    conn = sqlite3.connect("Admins.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        username TEXT PRIMARY KEY,
        password_hash TEXT
    )
    """)
    conn.commit()
    conn.close()
    
    conn = sqlite3.connect("Users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        firstname TEXT,
        lastname TEXT,
        birthdate DATE,
        gender TEXT,
        streetname TEXT,
        streetnumber TEXT,
        zipcode TEXT,
        city TEXT,
        email TEXT UNIQUE,
        mobilephone TEXT,
        drivinglicense TEXT
    )
    """)                   
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    SetupDB()
    print(Login.register("Username1", "Ab1234561111111!!")) #Will fail now because it is already in the database
    print(Login.login("Username", "Ab123456!!"))
    print(Login.login("Username1", "Ab1234561111111!!"))
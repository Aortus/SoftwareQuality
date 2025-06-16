import sqlite3
import bcrypt
# import re
import LoginUI


# === Setup database ===
def SetupDB():
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password_hash TEXT,
        naam TEXT
    )
    """)
    # To do: add a column for the type of admin (Super administrator, System administrator or Service engineer)
    conn.commit()
    cursor = conn.cursor()
    hashed = bcrypt.hashpw("Admin_123?".encode(), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO admins (username, password_hash, firstname, lastname, admin_type) VALUES (?, ?, ?, ?, ?)", ("super_admin", hashed, "Super", "Admin", "Super Administrator"))
    except sqlite3.IntegrityError:
        print("Admin user already exists.")
    conn.commit()
    conn.close()
    conn = sqlite3.connect("SQDB.db")
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
    # To do: make the user ID in another way               
    conn.commit()
    conn.close()

    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scooters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        in_servicedate DATETIME DEFAULT CURRENT_TIMESTAMP,
        brand TEXT,
        model TEXT,
        serialnumber TEXT UNIQUE,
        topspeed INTEGER,
        batterycapacity INTEGER,
        stateofcharge INTEGER,
        targetstateofcharge INTEGER,
        outofservice BOOLEAN,
        mileage INTEGER,
        lastmaintenance DATETIME,
        location TEXT
    )
    """)              
    conn.commit()
    conn.close()
    
    
if __name__ == "__main__":
    SetupDB()
    LoginUI.login_screen()

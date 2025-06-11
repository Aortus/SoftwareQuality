import sqlite3
import bcrypt
# import re
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
    # To do: add a column for the type of admin (Super administrator, System administrator or Service engineer)
    conn.commit()
    cursor = conn.cursor()
    hashed = bcrypt.hashpw("Admin_123?".encode(), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO admins (username, password_hash) VALUES (?, ?)", ("super_admin", hashed))
    except sqlite3.IntegrityError:
        print("Admin user already exists.")
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
    # To do: make the user ID in another way               
    conn.commit()
    conn.close()
    
    # To do: Make a db for the scooters
    
    
if __name__ == "__main__":
    SetupDB()
    print(Login.register("Username1", "Ab1234561111111!!")) #Will fail now because it is already in the database
    print(Login.login("Username", "Ab123456!!")) #should fail
    print(Login.login("Username1", "Ab1234561111111!!")) #should succeed
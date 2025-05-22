import sqlite3
import bcrypt
import re
import Login


# === Setup database ===
def SetupDB():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password_hash TEXT
    )
    """)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    SetupDB()
    print(Login.register("Username1", "Ab1234561111111!!")) #Will fail now because it is already in the database
    print(Login.login("Username", "Ab123456!!"))
    print(Login.login("Username1", "Ab1234561111111!!"))
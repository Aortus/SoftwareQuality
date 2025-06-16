import sqlite3
import bcrypt
import re
import datetime

def register(username, password, firstname, lastname, admintype):
    if not is_valid_username(username):
        return "Invalid username, try again! (Between 7 and 10 characters, start with a letter or underscore)"
    if not is_valid_password(password):
        return "Invalid password, try again! (atleast 12 characters, uppercase letter, lowercase letter, number, symbol and no more than 30 characters)" 

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) #Bcrypt hashes the password, to retrieve the password, you need to use bcrypt.checkpw()

    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO admins (username, password_hash, firstname, lastname, admin_type) VALUES (?, ?, ?, ?, ?)", (username, hashed, firstname, lastname, admintype))
        conn.commit()
        return "Admin succesfully registered"
    
    except:
        return "Admin registration failed"
    
def login(username, password):
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM admins WHERE username = ?", (username,))
    row = cursor.fetchone()
    if row and bcrypt.checkpw(password.encode(), row[0]): #Uses bcrypt to check the password, this is because the password is hashed
        return "Login succesful"
    else:
        return "Invalid username or password"

def is_valid_username(UN):
    username = UN.lower()
    if len(username) < 7 or len(username) > 10: #Length
        return False
    
    if re.match(r'^[A-Za-z_][A-Za-z0-9_\'\.]*$', username): #mathes the regex to the requirements
        return True
    else:
        return False

def is_valid_password(password):
    if len(password) < 12 or len(password) > 30: #Length
        return False
    if not re.search(r"[A-Z]", password): #Uppercase
        return False
    if not re.search(r"[a-z]", password): #Lowercase
        return False
    if not re.search(r"[0-9]", password): #Number
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): #Special char
        return False
    return True

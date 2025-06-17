import sqlite3
import bcrypt
import re
import Encryption
import datetime
import logger

def register(username, password, firstname, lastname, admintype):
    if not is_valid_username(username):
        return "Invalid username, try again! (Between 7 and 10 characters, start with a letter or underscore)"
    if not is_valid_password(password):
        return "Invalid password, try again! (atleast 12 characters, uppercase letter, lowercase letter, number, symbol and no more than 30 characters)" 

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) #Bcrypt hashes the password, to retrieve the password, you need to use bcrypt.checkpw()

    encrypted_username = Encryption.encrypt_data(username)
    encrypted_firstname = Encryption.encrypt_data(firstname)
    encrypted_lastname = Encryption.encrypt_data(lastname)
    encrypted_admintype = Encryption.encrypt_data(admintype)
    date = Encryption.encrypt_data(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO admins (username, password_hash, firstname, lastname, registration_date, admin_type) VALUES (?, ?, ?, ?, ?, ?)", (encrypted_username, hashed, encrypted_firstname, encrypted_lastname, date, encrypted_admintype))
        conn.commit()
        return "Admin succesfully registered"
    
    except:
        return "Admin registration failed"
    
def login(username, password):
    admins = Encryption.get_all_admins()
    for admin in admins:
        if admin[0] == username and bcrypt.checkpw(password.encode(), admin[1]):
            return "Login succesful"
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

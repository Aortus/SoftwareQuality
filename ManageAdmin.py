import sqlite3
import bcrypt
import Login
import datetime
import Encryption

# Getallusers retrieves all users from the database.
def get_all_admins():
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins")
    admins = cursor.fetchall()
    conn.close()

    decrypted_admins = []
    for admin in admins:
        admin_list = list(admin)
        for i in range(0, len(admin_list)):
            if i == 0 or i == 2:
                continue
            admin_list[i] = Encryption.decrypt_data(admin_list[i])
        decrypted_admins.append(tuple(admin_list))

    return decrypted_admins

def print_all_admins():
    admins = get_all_admins()

    for admin in admins:
        print(f"ID: {admin[0]} Username: {admin[1]} Voornaam: {admin[3]} Achternaam: {admin[4]} Registratie datum: {admin[5]} Admin Type: {admin[6]}")

def update_acc(username):
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()

    change = input(
        "Wat wilt u veranderen aan het account?\n"
        "1. Naam\n"
        "2. Username\n"
        "3. Wachtwoord\n"
        "4. Verwijderen\n"
        "Keuze: "
    ).lower()

    if change in ("1", "naam"):
        choice = input("Welke naam wilt u veranderen? (1. Voornaam / 2. Achternaam): ").lower()
        if choice in ("1", "voornaam", "voor"):
            new_firstname = input("Voer de nieuwe voornaam in (type Q om te stoppen): ")
            if new_firstname.lower() == "q":
                print("Wijzigen afgebroken.")
                return
            cursor.execute(
                "UPDATE admins SET firstname = ? WHERE username = ?",
                (new_firstname, username)
            )
            conn.commit()
            print(f"Voornaam gewijzigd naar: {new_firstname}")

        elif choice in ("2", "achternaam", "achter"):
            new_lastname = input("Voer de nieuwe achternaam in (type Q om te stoppen): ")
            if new_lastname.lower() == "q":
                print("Wijzigen afgebroken.")
                return
            cursor.execute(
                "UPDATE admins SET lastname = ? WHERE username = ?",
                (new_lastname, username)
            )
            conn.commit()
            print(f"Achternaam gewijzigd naar: {new_lastname}")

    elif change in ("2", "username"):
        new_username = ""
        while True:
            new_username = input("Wat moet de nieuwe username worden? (type Q om te stoppen): ")
            if new_username.lower() == "q":
                print("Wijzigen afgebroken.")
                break
            if(Login.is_valid_username(new_username)):
                cursor.execute(
                    "UPDATE admins SET username = ? WHERE username = ?",
                    (new_username, username)
                )
                conn.commit()
                print(f"Username gewijzigd naar: {new_username}")
                break

    elif change in ("3", "wachtwoord"):
        new_password = ""
        while True:
            new_password = input("Voer nieuw wachtwoord in (type Q om te stoppen): ")
            if(Login.is_valid_password(new_password)):
                hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
                cursor.execute(
                    "UPDATE admins SET password_hash = ? WHERE username = ?",
                    (hashed_pw, username)
                )
                conn.commit()
                print("Wachtwoord gewijzigd.")
    
    elif change in ("4", "verwijderen"):
        delete = input("Het terug halen van een account is alleen mogelijk door middel van het laden van een oude backup.\nType verwijder om door te gaan met verwijderen.")
        if(delete == "verwijder"):
            decrypted_admins = get_all_admins()
            for admin in decrypted_admins:
                if admin[1] == username:
                    row = admin

            if row:
                delete_entry_by_id(row[0]) 
            else:
                return None
        else:
            print("Ongeldige keuze.")

    conn.close()

def AddAdmin():
    go_on = ""
    while go_on.lower() != "q":
        new_username = input("Voer de nieuwe username in: ")
        new_password = input("Voer het nieuwe wachtwoord in: ")
        new_firstname = input("Voer de voornaam in: ")
        new_lastname = input("Voer de achternaam in: ")
        admintype = input("Voer het admin type in ('1. System Administrator', '2. Service Engineer'): ").lower()
        if admintype in ("1", "system administrator", "systemadmin"):
            new_admintype = "System Administrator"
        elif admintype in ("2", "service engineer", "serviceengineer"):
            new_admintype = "Service Engineer"
        else:
            print("Ongeldige admin type. Probeer het opnieuw.")
            go_on = input("Druk op Enter om opnieuw te proberen of type 'q' om af te breken: ")

        if (Login.register(new_username, new_password, new_firstname, new_lastname, new_admintype) != "Admin succesfully registered"):
            print("Er is iets fout gegaan bij het toevoegen van de admin. Probeer het opnieuw.")
            go_on = input("Druk op Enter om opnieuw te proberen of type 'q' om af te breken: ")
        
        else:
            go_on = "q"

def delete_entry_by_id(table_name, entry_id):
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()

    sql = f"DELETE FROM {table_name} WHERE id = ?"
    cursor.execute(sql, (entry_id,))

    conn.commit()
    conn.close()

    return f"Account met {entry_id} verwijderd van '{table_name}'."

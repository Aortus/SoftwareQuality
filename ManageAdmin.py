import sqlite3
import bcrypt
import Login
import datetime
import Encryption
from time import sleep
import Logs
import LoginUI

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
    user_id = get_id_by_username(username)

    change = input(
        "\nWat wilt u veranderen aan het account?\n"
        "1. Naam\n"
        "2. Username\n"
        "3. Wachtwoord\n"
        "4. Verwijderen\n"
        "5. Terug\n"
        "Keuze: "
    ).lower()

    if Login.has_null_byte(change):
        print("Ongeldige invoer. Probeer het opnieuw.")
        return

    if change in ("1", "naam"):
        choice = input("Welke naam wilt u veranderen? (1. Voornaam / 2. Achternaam): ").lower()
        if choice in ("1", "voornaam", "voor"):
            new_firstname = input("Voer de nieuwe voornaam in (type Q om te stoppen): ")
            if new_firstname.lower() == "q":
                print("Wijzigen afgebroken.")
                return
            new_firstname_enc = Encryption.encrypt_data(new_firstname)
            cursor.execute(
                "UPDATE admins SET firstname = ? WHERE id = ?",
                (new_firstname_enc, user_id)
            )
            conn.commit()
            print(f"Voornaam gewijzigd naar: {new_firstname}")
            Logs.log_activity(username, "Name Change", f"Voornaam gewijzigd naar: {new_firstname}", 0)
            sleep(1)

        elif choice in ("2", "achternaam", "achter"):
            new_lastname = input("Voer de nieuwe achternaam in (type Q om te stoppen): ")
            if new_lastname.lower() == "q":
                print("Wijzigen afgebroken.")
                return
            new_lastname_enc = Encryption.encrypt_data(new_lastname)
            cursor.execute(
                "UPDATE admins SET lastname = ? WHERE id = ?",
                (new_lastname_enc, user_id)
            )
            conn.commit()
            print(f"Achternaam gewijzigd naar: {new_lastname}")
            Logs.log_activity(username, "Name Change", f"Achternaam gewijzigd naar: {new_lastname}", 0)

    elif change in ("2", "username"):
        new_username = ""
        while True:
            new_username = input("Wat moet de nieuwe username worden? (type Q om te stoppen): ")
            if new_username.lower() == "q":
                print("Wijzigen afgebroken.")
                break
            if(Login.is_valid_username(new_username)):
                new_username_enc = Encryption.encrypt_data(new_username)
                cursor.execute(
                    "UPDATE admins SET username = ? WHERE id = ?",
                    (new_username_enc, user_id)
                )
                conn.commit()
                print(f"Username gewijzigd naar: {new_username}")
                Logs.log_activity(username, "Username Change", f"username gewijzigd van {username} naar: {new_username}", 0)
                break

    elif change in ("3", "wachtwoord"):
        new_password = ""
        while True:
            new_password = input("Voer nieuw wachtwoord in (type Q om te stoppen): ")
            if(Login.is_valid_password(new_password)):
                new_password = "temp" + new_password
                hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
                cursor.execute(
                    "UPDATE admins SET password_hash = ? WHERE id = ?",
                    (hashed_pw, user_id)
                )
                conn.commit()
                print("Wachtwoord gewijzigd.")
                print("Let op: Dit is een tijdelijk wachtwoord, u moet het later wijzigen.")
                print(new_password)
                Logs.log_activity(username, "Password change", f"Wachtwoord gereset van {username}", 0)

                sleep(5)
                
            elif new_password.lower() == "q":
                print("Wijzigen afgebroken.")
                break
    
    elif change in ("4", "verwijderen"):
        delete = input("Het terug halen van een account is alleen mogelijk door middel van het laden van een oude backup.\nType verwijder om door te gaan met verwijderen.")
        if(delete == "verwijder"):
            decrypted_admins = get_all_admins()
            for admin in decrypted_admins:
                if admin[1] == username:
                    row = admin

            if row:
                delete_entry_by_id(row[0]) 
                Logs.log_activity(username, "Account verwijderd", f"Account van {username} gewijzigd", 0)

            else:
                Logs.log_activity(username, "Account verwijderen gefaald", f"{username} geprobeerd om account te verwijderen", 1)
                return None
                

    elif change in ("5", "terug", "q"):
        print("Terug naar het hoofdmenu.")
        return
    else:
        print("Ongeldige keuze.")

    conn.close()

def change_password(username):
    admins = get_all_admins()
    for admin in admins:
        if admin[1] == username:
            conn = sqlite3.connect("SQDB.db")
            cursor = conn.cursor()
            adminid = admin[0]
            new_password = input("Voer nieuw wachtwoord in (type Q om te stoppen): ")
            if(Login.is_valid_password(new_password)):
                hashed_pw = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
                cursor.execute(
                    "UPDATE admins SET password_hash = ? WHERE id = ?",
                    (hashed_pw, adminid)
                )
                conn.commit()
                print("Wachtwoord gewijzigd.")
                Logs.log_activity(username, "Password change", f"Wachtwoord gereset van {username}", 0)
                sleep(5)
            elif new_password.lower() == "q":
                print("Wijzigen afgebroken.")
            else:
                print("Ongeldig wachtwoord. Probeer het opnieuw.")
            conn.close()
            return

def AddAdmin(): 
    go_on = ""
    while go_on != "q":
        print("Let op: De username moet tussen de 7 en 10 karakters lang zijn")
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
            Logs.log_activity(new_username, "Admin toevoegen gefaald", "Ongeldige admin type ingevoerd", 1)
            go_on = input("Druk op Enter om opnieuw te proberen of type 'q' om af te breken: ")
            continue

        result = Login.register(new_username, new_password, new_firstname, new_lastname, new_admintype)
        if result != "Admin succesfully registered":
            print("Er is iets fout gegaan bij het toevoegen van de admin. Probeer het opnieuw.")
            Logs.log_activity(new_username, "Admin toevoegen gefaald", "Er is iets fout gegaan bij het toevoegen van de admin", 1)
            go_on = input("Druk op Enter om opnieuw te proberen of type 'q' om af te breken: ")
        else:
            print("Admin succesvol toegevoegd.")
            Logs.log_activity(new_username, "Admin toegevoegd", f"Admin {new_username} succesvol toegevoegd", 0)
            input("Druk op Enter om door te gaan of type 'q' om af te breken: ")
            go_on = "q"


def delete_entry_by_id(table_name, entry_id):
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()

    sql = f"DELETE FROM {table_name} WHERE id = ?"
    cursor.execute(sql, (entry_id,))

    conn.commit()
    conn.close()

    return f"Account met {entry_id} verwijderd van '{table_name}'."

def get_id_by_username(username_plain):
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM admins")
    rows = cursor.fetchall()
    conn.close()

    for admin_id, encrypted_username in rows:
        decrypted_username = Encryption.decrypt_data(encrypted_username)
        if decrypted_username == username_plain:
            return admin_id
    return None

def get_admin_by_username(username_plain):
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, admin_type FROM admins")
    rows = cursor.fetchall()
    conn.close()

    for admin_id, encrypted_username, encrypted_admin_type in rows:
        decrypted_username = Encryption.decrypt_data(encrypted_username)
        decrypted_admin_type = Encryption.decrypt_data(encrypted_admin_type)
        if decrypted_username == username_plain:
            return {"id": admin_id, "admin_type": decrypted_admin_type}
    return None

def update_own_acc(username):
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()

    change = input(
        "\nWat wilt u veranderen aan het account?\n"
        "1. Naam\n"
        "2. Username\n"
        "3. Wachtwoord\n"
        "4. Verwijderen\n"
        "5. Terug\n"
        "Keuze: "
    ).lower()

    if Login.has_null_byte(change):
        print("Ongeldige invoer. Probeer het opnieuw.")
        return username

    if change in ("1", "naam"):
        choice = input("Welke naam wilt u veranderen? (1. Voornaam / 2. Achternaam): ").lower()
        if choice in ("1", "voornaam", "voor"):
            new_firstname = input("Voer de nieuwe voornaam in (type Q om te stoppen): ")
            if new_firstname.lower() == "q":
                print("Wijzigen afgebroken.")
                return username
            cursor.execute(
                "UPDATE admins SET firstname = ? WHERE username = ?",
                (new_firstname, username)
            )
            conn.commit()
            print(f"Voornaam gewijzigd naar: {new_firstname}")
            Logs.log_activity(username, "Name Change", f"Voornaam gewijzigd naar: {new_firstname}", 0)
            input("Druk op Enter om terug te gaan.")
            return username

        elif choice in ("2", "achternaam", "achter"):
            new_lastname = input("Voer de nieuwe achternaam in (type Q om te stoppen): ")
            if new_lastname.lower() == "q":
                print("Wijzigen afgebroken.")
                return username
            cursor.execute(
                "UPDATE admins SET lastname = ? WHERE username = ?",
                (new_lastname, username)
            )
            conn.commit()
            print(f"Achternaam gewijzigd naar: {new_lastname}")
            Logs.log_activity(username, "Name Change", f"Achternaam gewijzigd naar: {new_lastname}", 0)
            input("Druk op Enter om terug te gaan.")
            return username

    elif change in ("2", "username"):
        while True:
            new_username = input("Wat moet de nieuwe username worden? (type Q om te stoppen): ")
            if new_username.lower() == "q":
                print("Wijzigen afgebroken.")
                conn.close()
                return username
            if Login.is_valid_username(new_username):
                admins = get_all_admins()
                for admin in admins:
                    if admin[1] == username:
                        conn = sqlite3.connect("SQDB.db")
                        cursor = conn.cursor()
                        adminid = admin[0]
                enc_new_username = Encryption.encrypt_data(new_username)
                cursor.execute(
                    "UPDATE admins SET username = ? WHERE id = ?",
                    (enc_new_username, adminid)
                )
                conn.commit()
                print(f"Username gewijzigd naar: {new_username}")
                Logs.log_activity(username, "Username Change", f"username gewijzigd van {username} naar: {new_username}", 0)
                sleep(1)
                conn.close()
                return new_username
            else:
                print("Ongeldige username. Probeer het opnieuw.")


    elif change in ("3", "wachtwoord"):
        new_password = input("Nieuw wachtwoord: ")
        if Login.is_valid_password(new_password):
            Login.change_password(username, new_password)
            input("Wachtwoord succesvol gewijzigd. Druk op Enter om terug te keren.")
            return username
        else:
            input("Ongeldig wachtwoord. Zorg ervoor dat het minstens 12 tekens lang is, een hoofdletter, een kleine letter, een cijfer en een speciaal teken bevat. Druk op Enter om opnieuw te proberen.")
            return username
    elif change in ("4", "verwijderen"):
        print("Weet u zeker dat u dit account wilt verwijderen? Dit kan niet ongedaan worden gemaakt.")
        confirm = input("Typ 'ja' om te bevestigen: ").strip().lower()
        if confirm == 'ja':
            user_id = get_id_by_username(username)
            print(delete_entry_by_id("admins", user_id))
            print("Account succesvol verwijderd.")
            input("Druk op Enter om terug te keren naar het inlogscherm.")
            LoginUI.login_screen()
            return None
    elif change in ("5", "terug", "q"):
        print("Terug naar het hoofdmenu.")
        return username
    else:
        print("Ongeldige keuze.")
        return username
import sqlite3
import bcrypt
import Login
import sqlite3

# Getallusers retrieves all users from the database.
def get_all_users():
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins")
    users = cursor.fetchall()
    conn.close()
    return users

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
            cursor.execute("SELECT id FROM admins WHERE username = ?", (username,))
            row = cursor.fetchone()
            conn.close()

            if row:
                delete_entry_by_id(row[0]) 
            else:
                return None
    else:
        print("Ongeldige keuze.")

    conn.close()

def delete_entry_by_id(table_name, entry_id): #To do, een find id with username
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()

    # Use parameterized query to avoid SQL injection
    sql = f"DELETE FROM {table_name} WHERE id = ?"
    cursor.execute(sql, (entry_id,))

    conn.commit()
    conn.close()

    print(f"Deleted entry with ID {entry_id} from table '{table_name}'.")


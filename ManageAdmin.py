import sqlite3
import bcrypt
import Login
import sqlite3

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
        new_name = ""
        while True:
            new_name = input("Wat moet de nieuwe naam worden? (type Q om te stoppen): ")
            if new_name.lower() == "q":
                print("Wijzigen afgebroken.")
                break
            # if(Login.is_valid_username(new_name)): Hier moet een nieuwe naam checker komen
            cursor.execute(
                "UPDATE admins SET naam = ? WHERE username = ?",
                (new_name, username)
            )
            conn.commit()
            print(f"Naam gewijzigd naar: {new_name}")
            break

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


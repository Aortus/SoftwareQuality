import Encryption
from datetime import datetime
import sqlite3
import shutil
import os
import Logs

def backup_database(password):
    import sqlite3
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H_%M")
    backup_file = f"SQDB_backup_{timestamp}.db"
    source = sqlite3.connect("SQDB.db")
    backup = sqlite3.connect(backup_file)
    with backup:
        source.backup(backup)
    source.close()
    hashed = Encryption.hash_password(password)
    cursor = backup.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS backup_info (
            id INTEGER PRIMARY KEY,
            password TEXT,
            datetime DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restore_codes (
            id INTEGER PRIMARY KEY,
            password TEXT,
            username TEXT,
            datetime DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cursor.execute("""
        INSERT INTO backup_info (password, datetime) VALUES (?, ?)
    """, (hashed, timestamp))
    backup.commit()
    backup.close()
    print(f"Backup gemaakt in file {backup_file}")
    return backup_file



def restore_database_from_backup(backup_file):
    temp_backup_file = backup_file + ".temp.db"
    shutil.copy(backup_file, temp_backup_file)

    temp_backup = sqlite3.connect(temp_backup_file)
    temp_cursor = temp_backup.cursor()
    temp_cursor.execute("DROP TABLE IF EXISTS backup_info")
    temp_cursor.execute("DROP TABLE IF EXISTS restore_codes")
    temp_backup.commit()

    main = sqlite3.connect("SQDB.db")
    with main:
        temp_backup.backup(main)

    temp_backup.close()
    main.close()
    os.remove(temp_backup_file)

    print(f"Hoofd database hersteld van {backup_file}")
    Logs.log_activity("System", "Database Restore", f"Database hersteld van back-up {backup_file}", 0)

def restore_database_from_password(backup_file, password):
    backup = sqlite3.connect(backup_file)
    cursor = backup.cursor()
    cursor.execute("SELECT password FROM backup_info LIMIT 1")
    row = cursor.fetchone()
    if not row:
        print("Geen wachtwoord gevonden in de back-up.")
        backup.close()
        return

    password_hash = row[0]
    if not Encryption.check_password(password_hash, password):
        print("Ongeldig wachtwoord voor back-up herstel.")
        backup.close()
        return "Ongeldig wachtwoord"

    backup.close()

    restore_database_from_backup(backup_file)

def restore_backup_through_code(backup_file, restore_code, username):
    conn = sqlite3.connect(backup_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restore_codes")
    row = cursor.fetchone()
    if not row:
        print(f"Geen herstelcode gevonden voor gebruiker {username} in back-up {backup_file}")
        conn.close()
        return

    if not Encryption.check_password(row[1], restore_code):
        print("Ongeldige herstelcode.")
        conn.close()
        return
    else:
        restore_id = row[0]

        cursor.execute("""
            DELETE FROM restore_codes WHERE id = ?
        """, (restore_id,))
        restore_database_from_backup(backup_file)
        conn.commit()
        conn.close()
        print(f"Back-up hersteld voor gebruiker {username} met herstelcode {restore_code}")

def create_restore_code(backup_file, password, username):
    Encryptun = Encryption.encrypt_data(username)
    hashed = Encryption.hash_password(password)
    conn = sqlite3.connect(backup_file)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO restore_codes (password, username) VALUES (?, ?)
    """, (hashed, Encryptun))
    conn.commit()
    conn.close()
    print (f"Herstelcode aangemaakt voor gebruiker {username} in back-up {backup_file}")

def delete_restore_code(backup_file, username):
    conn = sqlite3.connect(backup_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restore_codes")
    rows = cursor.fetchall()
    conn.close()
    for row in rows:
        un = Encryption.decrypt_data(row[2])
        if un == username:
            id = row[0]
            break
    conn = sqlite3.connect(backup_file)
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM restore_codes WHERE id = ?
    """, (id,))
    conn.commit()
    conn.close()
    print(f"Herstelcode verwijderd voor gebruiker {username} in back-up {backup_file}")

# Voorbeeld gebruik:
# backup_file = backup_database(password)
# restore_database_from_backup(backup_file, password)

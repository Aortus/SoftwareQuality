import Encryption
from datetime import datetime
import sqlite3
import shutil
import os

def backup_database(password):
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
        )
    """)
    cursor.execute("""
        INSERT INTO backup_info (password, datetime) VALUES (?, ?)
    """, (hashed, timestamp))
    backup.commit()
    backup.close()
    print(f"Back up gemaakt in file {backup_file}")
    return backup_file

def restore_database_from_backup(backup_file, password):
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
        return

    backup.close()

    temp_backup_file = backup_file + ".temp.db"
    shutil.copy(backup_file, temp_backup_file)

    temp_backup = sqlite3.connect(temp_backup_file)
    temp_cursor = temp_backup.cursor()
    temp_cursor.execute("DROP TABLE IF EXISTS backup_info")
    temp_backup.commit()

    main = sqlite3.connect("SQDB.db")
    with main:
        temp_backup.backup(main)

    temp_backup.close()
    main.close()
    os.remove(temp_backup_file)

    print(f"Hoofd database hersteld van {backup_file}")

# Voorbeeld gebruik:
# backup_file = backup_database(password)
# restore_database_from_backup(backup_file, password)

import Encryption
import sqlite3

def log_activity(username, action, details, is_suspicious=0):
    encrypted_username = Encryption.encrypt_data(username)
    encrypted_action = Encryption.encrypt_data(action)
    encrypted_details = Encryption.encrypt_data(details)
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (user_id, action, details, is_suspicious)
        VALUES (?, ?, ?, ?)
    """, (encrypted_username, encrypted_action, encrypted_details, is_suspicious))
    conn.commit()
    conn.close()

def get_unread_logs():
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, user_id, action, details, is_suspicious, is_read
        FROM logs 
        WHERE is_read = 0
    """)
    rows = cursor.fetchall()

    decrypted = []
    read_ids = []

    for row in rows:
        decrypted.append((
            row[0],  # id
            row[1],  # timestamp
            Encryption.decrypt_data(row[2]),  # user_id
            Encryption.decrypt_data(row[3]),  # action
            Encryption.decrypt_data(row[4]),  # details
            "suspicious" if row[5] == 1 else "safe",  # is_suspicious
        ))
        read_ids.append(row[0])

    if read_ids:
        cursor.executemany(
            "UPDATE logs SET is_read = 1 WHERE id = ?",
            [(log_id,) for log_id in read_ids]
        )
        conn.commit()

    conn.close()
    return decrypted

def get_all_logs():
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    rows = cursor.fetchall()
    conn.close()

    # Decrypt content
    decrypted = []
    for row in rows:
        decrypted.append((
            row[0],  # id
            row[1],  # timestamp
            Encryption.decrypt_data(row[2]),  # user_id
            Encryption.decrypt_data(row[3]),  # action
            Encryption.decrypt_data(row[4]),  # details
            "suspicious" if row[5] == 1 else "safe",  # is_suspicious
            "read" if row[6] == 1 else "unread"       # is_read
        ))
    return decrypted

def check_unread_suspicious_logs():
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM logs
        WHERE is_read = 0 AND is_suspicious = 1
    """)
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0

def get_unread_suspicious_logs():
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, user_id, action, details, is_suspicious
        FROM logs 
        WHERE is_read = 0 AND is_suspicious = 1
    """)
    rows = cursor.fetchall()

    decrypted = []
    read_ids = []

    for row in rows:
        decrypted.append(( 
            row[0],  # id
            row[1],  # timestamp
            Encryption.decrypt_data(row[2]),
            Encryption.decrypt_data(row[3]),
            Encryption.decrypt_data(row[4]),
            "suspicious" if row[5] == 1 else "safe"
        ))
        read_ids.append(row[0])

    if read_ids:
        cursor.executemany(
            "UPDATE logs SET is_read = 1 WHERE id = ?",
            [(log_id,) for log_id in read_ids]
        )
        conn.commit()

    conn.close()
    return decrypted
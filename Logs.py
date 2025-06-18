import Encryption
import sqlite3

def log_activity(user_id, action, details, is_suspicious=0):
    encrypted_action = Encryption.encrypt_data(action)
    encrypted_details = Encryption.encrypt_data(details)
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (user_id, action, details, is_suspicious)
        VALUES (?, ?, ?, ?)
    """, (user_id, encrypted_action, encrypted_details, is_suspicious))
    conn.commit()
    conn.close()

def get_unread_suspicious_logs():
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, action, details 
        FROM logs 
        WHERE is_suspicious = 1 AND is_read = 0
    """)
    rows = cursor.fetchall()
    conn.close()

    # Decrypt content
    decrypted = []
    read_ids = []
    for row in rows:
        decrypted.append((
            row[0],  # id
            row[1],  # timestamp
            Encryption.decrypt_data(row[2]), # action  
            Encryption.decrypt_data(row[3])  # details
        ))
        read_ids.append(row[0])
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
            row[2],  # user_id
            Encryption.decrypt_data(row[3]),  # action
            Encryption.decrypt_data(row[4]),  # details
            row[5],  # is_suspicious
            row[6]   # is_read
        ))
    return decrypted

def mark_logs_as_read(log_ids):
    conn = sqlite3.connect("SQDB.db")
    cursor = conn.cursor()
    cursor.executemany("""
        UPDATE logs SET is_read = 1 WHERE id = ?
    """, [(log_id,) for log_id in log_ids])
    conn.commit()
    conn.close()

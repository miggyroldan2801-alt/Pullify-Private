import sqlite3

def init_db():
    conn = sqlite3.connect('pullify.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs 
                      (user_id INTEGER, ip_hash TEXT, status TEXT, timestamp DATETIME)''')
    conn.commit()
    conn.close()

def log_verification(ip_hash, user_id, status):
    # Logic to insert into DB
    pass

def is_banned(user_id, ip_hash):
    # Logic to check if user or IP is banned
    return False

init_db()
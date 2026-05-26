import sqlite3

def init_db():
    conn = sqlite3.connect('pullify.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs 
                      (user_id INTEGER, ip_hash TEXT, status TEXT, timestamp DATETIME)''')
    conn.commit()
    conn.close()

# Call this once at startup if needed
init_db()
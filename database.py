import sqlite3

# Initialize the database
def init_db():
    conn = sqlite3.connect('pullify.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS logs 
                      (user_id INTEGER, ip_hash TEXT, status TEXT, timestamp DATETIME)''')
    conn.commit()
    conn.close()

# The specific functions the bot needs
def log_verification(ip_hash, user_id, status):
    conn = sqlite3.connect('pullify.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (user_id, ip_hash, status, timestamp) VALUES (?, ?, ?, CURRENT_TIMESTAMP)", 
                   (user_id, ip_hash, status))
    conn.commit()
    conn.close()

def is_banned(user_id, ip_hash):
    # Add your logic here, for now returning False
    return False

# Run this once on import to ensure table exists
init_db()
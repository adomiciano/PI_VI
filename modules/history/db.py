import sqlite3

def create_connection():
    conn = sqlite3.connect('./db/pi.db')

    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            has_person BOOLEAN NOT NULL,
            has_hardhat BOOLEAN NOT NULL,
            employee_name TEXT NULL
        )
    ''')

    conn.commit()

    return conn
    
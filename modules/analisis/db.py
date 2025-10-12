import sqlite3
from pathlib import Path
from contextlib import contextmanager

@contextmanager
def create_connection():
    """Create a database connection to a SQLite database."""
    # Create the database directory if it doesn't exist
    db_dir = Path("./db")
    db_dir.mkdir(exist_ok=True)
    
    conn = sqlite3.connect("./db/analysis.db")
    try:
        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON")
        # Create tables if they don't exist
        conn.execute("""
        CREATE TABLE IF NOT EXISTS analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL,
            has_person BOOLEAN NOT NULL,
            has_hardhat BOOLEAN NOT NULL,
            employee_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
        yield conn
    finally:
        conn.close()

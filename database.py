# database.py
import sqlite3
from datetime import datetime

DATABASE_NAME = 'tasks.db'

def connect_db():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

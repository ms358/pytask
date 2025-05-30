# database.py
import sqlite3
from datetime import datetime

DATABASE_NAME = 'tasks.db'

def connect_db():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        conn.row_factory = sqlite3.Row
        print("Database connection established.")
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

def create_table():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                ''')
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            conn.commit()
            conn.close()

def add_task(description):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''INSERT INTO tasks (description) VALUES (?)''', (description,))
            conn.commit()
            conn.close()
            print("Task added successfully.")
        except sqlite3.Error as e:
            conn.close()
            print(f"Error adding task: {e}")

def get_tasks(status=None):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        if status:
            cursor.execute('''SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC''', (status,))
        else:
            cursor.execute('''SELECT * FROM tasks ORDER BY created_at DESC''')
        tasks = cursor.fetchall()
        conn.close()
        return tasks

def update_task(task_id, new_status):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''UPDATE tasks SET status = ? WHERE id = ?''', (new_status, task_id))
            conn.commit()
            conn.close()
            if cursor.rowcount == 0:
                print("No task found with the given ID.")
            else:
                print("Task updated successfully.")
        except sqlite3.Error as e:
            conn.close()
            print(f"Error updating task: {e}")

def delete_task(task_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''DELETE FROM tasks WHERE id = ?''', (task_id,))
            conn.commit()
            conn.close()
            if cursor.rowcount == 0:
                print("No task found with the given ID.")
            else:
                print("Task deleted successfully.")
        except sqlite3.Error as e:
            conn.close()
            print(f"Error deleting task: {e}")

if __name__ == "__main__":
    create_table()
    print("Database setup complete.")

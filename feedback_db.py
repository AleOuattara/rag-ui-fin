import sqlite3
from datetime import datetime

DB_PATH = "feedbacks.db"

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS feedbacks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                response TEXT,
                feedback TEXT,
                lang TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

def save_feedback(question: str, response: str, feedback: str, lang: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            INSERT INTO feedbacks (question, response, feedback, lang)
            VALUES (?, ?, ?, ?)
        ''', (question, response, feedback, lang))

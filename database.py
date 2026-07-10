import sqlite3
from datetime import datetime


DATABASE_NAME = "history.db"


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            score REAL,
            skills TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_analysis(score, skills):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO analyses (date, score, skills)
        VALUES (?, ?, ?)
        """,
        (
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            score,
            ", ".join(skills)
        )
    )

    connection.commit()
    connection.close()


def get_history():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, date, score, skills
        FROM analyses
        ORDER BY id ASC
    """)

    history = cursor.fetchall()

    connection.close()

    return history
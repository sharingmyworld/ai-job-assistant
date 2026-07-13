import sqlite3
from datetime import datetime


DATABASE_NAME = "history.db"


def create_database():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT,

            date TEXT,

            score REAL,

            skills TEXT

        )
    """)

    connection.commit()
    connection.close()


def save_analysis(
    username,
    score,
    skills
):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(

        """
        INSERT INTO analyses
        (
            username,
            date,
            score,
            skills
        )
        VALUES (?, ?, ?, ?)
        """,

        (

            username,

            datetime.now().strftime(
                "%Y-%m-%d %H:%M"
            ),

            score,

            ", ".join(skills)

        )

    )

    connection.commit()
    connection.close()


def get_history(username):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(

        """
        SELECT
            id,
            date,
            score,
            skills

        FROM analyses

        WHERE username=?

        ORDER BY id DESC
        """,

        (
            username,
        )

    )

    history = cursor.fetchall()

    connection.close()

    return history


def get_statistics(username):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*),
            AVG(score),
            MAX(score)
        FROM analyses
        WHERE username=?
        """,
        (
            username,
        )
    )

    result = cursor.fetchone()

    connection.close()

    return result

def get_progress(username):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(

        """
        SELECT
            date,
            score

        FROM analyses

        WHERE username=?

        ORDER BY id
        """,

        (
            username,
        )

    )

    data = cursor.fetchall()

    connection.close()

    return data

def delete_analysis(analysis_id):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(

        """
        DELETE FROM analyses
        WHERE id=?
        """,

        (
            analysis_id,
        )

    )

    connection.commit()
    connection.close()
    
def get_better_than_percentage(username, score):

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT score
        FROM analyses
        WHERE username=?
        """,
        (username,)
    )

    rows = cursor.fetchall()

    connection.close()

    scores = [
        row[0]
        for row in rows
    ]

    if len(scores) <= 1:
        return 0

    previous_scores = scores[:-1]

    better_count = sum(
        1
        for previous_score in previous_scores
        if score > previous_score
    )

    percentage = (
        better_count
        / len(previous_scores)
    ) * 100

    return percentage
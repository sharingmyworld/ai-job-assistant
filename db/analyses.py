from datetime import datetime

from .connection import get_connection
from .learning import create_learning_plan_table


def create_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id BIGSERIAL PRIMARY KEY,
            username TEXT,
            date TEXT,
            score REAL,
            skills TEXT,
            job_title TEXT DEFAULT '',
            missing_skills TEXT DEFAULT ''
        )
    """)

    cursor.execute(
        "ALTER TABLE analyses "
        "ADD COLUMN IF NOT EXISTS job_title TEXT DEFAULT ''"
    )
    cursor.execute(
        "ALTER TABLE analyses "
        "ADD COLUMN IF NOT EXISTS missing_skills TEXT DEFAULT ''"
    )
    cursor.execute(
        "ALTER TABLE analyses "
        "ADD COLUMN IF NOT EXISTS cv_version TEXT DEFAULT ''"
    )

    connection.commit()
    connection.close()

    create_learning_plan_table()


def save_analysis(
    username,
    score,
    skills,
    job_title="",
    missing_skills=None,
    cv_version=""
):
    if missing_skills is None:
        missing_skills = []

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO analyses
        (
            username,
            date,
            score,
            skills,
            job_title,
            missing_skills,
            cv_version
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            username,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            score,
            ", ".join(skills),
            job_title.strip(),
            ", ".join(missing_skills),
            cv_version.strip()
        )
    )

    connection.commit()
    connection.close()


def get_history(username):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, date, score, skills
        FROM analyses
        WHERE username=?
        ORDER BY id DESC
        """,
        (username,)
    )

    history = cursor.fetchall()
    connection.close()

    return history


def get_history_with_title(username):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            date,
            score,
            skills,
            COALESCE(job_title, ''),
            COALESCE(missing_skills, ''),
            COALESCE(cv_version, '')
        FROM analyses
        WHERE username=?
        ORDER BY id DESC
        """,
        (username,)
    )

    history = cursor.fetchall()
    connection.close()

    return history


def get_statistics(username):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*), AVG(score), MAX(score)
        FROM analyses
        WHERE username=?
        """,
        (username,)
    )

    result = cursor.fetchone()
    connection.close()

    return result


def get_progress(username):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT date, score
        FROM analyses
        WHERE username=?
        ORDER BY id
        """,
        (username,)
    )

    data = cursor.fetchall()
    connection.close()

    return data


def delete_analysis(analysis_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM analyses
        WHERE id=?
        """,
        (analysis_id,)
    )

    connection.commit()
    connection.close()


def get_better_than_percentage(username, score):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT score
        FROM analyses
        WHERE username=?
        ORDER BY id
        """,
        (username,)
    )

    rows = cursor.fetchall()
    connection.close()

    scores = [row[0] for row in rows]

    if len(scores) <= 1:
        return 0

    previous_scores = scores[:-1]

    better_count = sum(
        1
        for previous_score in previous_scores
        if score > previous_score
    )

    return (
        better_count / len(previous_scores)
    ) * 100

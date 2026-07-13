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
            skills TEXT,
            job_title TEXT DEFAULT '',
            missing_skills TEXT DEFAULT ''
        )
    """)

    cursor.execute("PRAGMA table_info(analyses)")

    columns = {
        row[1]
        for row in cursor.fetchall()
    }

    if "job_title" not in columns:
        cursor.execute(
            """
            ALTER TABLE analyses
            ADD COLUMN job_title TEXT DEFAULT ''
            """
        )

    if "missing_skills" not in columns:
        cursor.execute(
            """
            ALTER TABLE analyses
            ADD COLUMN missing_skills TEXT DEFAULT ''
            """
        )

    connection.commit()
    connection.close()

    create_learning_plan_table()


def save_analysis(
    username,
    score,
    skills,
    job_title="",
    missing_skills=None
):
    if missing_skills is None:
        missing_skills = []

    connection = sqlite3.connect(DATABASE_NAME)
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
            missing_skills
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            username,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            score,
            ", ".join(skills),
            job_title.strip(),
            ", ".join(missing_skills)
        )
    )

    connection.commit()
    connection.close()


def get_history(username):
    connection = sqlite3.connect(DATABASE_NAME)
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
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            date,
            score,
            skills,
            COALESCE(job_title, ''),
            COALESCE(missing_skills, '')
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
    connection = sqlite3.connect(DATABASE_NAME)
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
    connection = sqlite3.connect(DATABASE_NAME)
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
    connection = sqlite3.connect(DATABASE_NAME)
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
    connection = sqlite3.connect(DATABASE_NAME)
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



def create_learning_plan_table():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_plan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            skill TEXT NOT NULL,
            priority TEXT NOT NULL DEFAULT 'Średni',
            status TEXT NOT NULL DEFAULT 'Do nauki',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(username, skill)
        )
    """)

    connection.commit()
    connection.close()


def _get_skill_priority(skill):
    high_priority = {
        "python", "sql", "java", "javascript",
        "typescript", "git", "docker", "aws",
        "azure", "excel", "power bi", "tableau",
        "react", "django", "flask", "linux"
    }

    medium_priority = {
        "kubernetes", "pandas", "numpy",
        "machine learning", "rest api", "api",
        "html", "css", "node.js", "node",
        "postgresql", "mysql", "mongodb",
        "scrum", "agile"
    }

    normalized = skill.strip().lower()

    if normalized in high_priority:
        return "Wysoki"

    if normalized in medium_priority:
        return "Średni"

    return "Niski"


def add_skills_to_learning_plan(username, skills):
    create_learning_plan_table()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    for skill in skills:
        clean_skill = str(skill).strip()

        if not clean_skill:
            continue

        cursor.execute(
            """
            INSERT OR IGNORE INTO learning_plan
            (
                username,
                skill,
                priority,
                status,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, 'Do nauki', ?, ?)
            """,
            (
                username,
                clean_skill,
                _get_skill_priority(clean_skill),
                now,
                now
            )
        )

    connection.commit()
    connection.close()


def get_learning_plan(username):
    create_learning_plan_table()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            skill,
            priority,
            status,
            created_at,
            updated_at
        FROM learning_plan
        WHERE username=?
        ORDER BY
            CASE priority
                WHEN 'Wysoki' THEN 1
                WHEN 'Średni' THEN 2
                ELSE 3
            END,
            id DESC
        """,
        (username,)
    )

    rows = cursor.fetchall()
    connection.close()

    return rows


def update_learning_status(task_id, status):
    allowed_statuses = {
        "Do nauki",
        "W trakcie",
        "Ukończone"
    }

    if status not in allowed_statuses:
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE learning_plan
        SET status=?, updated_at=?
        WHERE id=?
        """,
        (
            status,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            task_id
        )
    )

    connection.commit()
    connection.close()


def update_learning_priority(task_id, priority):
    allowed_priorities = {
        "Wysoki",
        "Średni",
        "Niski"
    }

    if priority not in allowed_priorities:
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE learning_plan
        SET priority=?, updated_at=?
        WHERE id=?
        """,
        (
            priority,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            task_id
        )
    )

    connection.commit()
    connection.close()


def delete_learning_task(task_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM learning_plan
        WHERE id=?
        """,
        (task_id,)
    )

    connection.commit()
    connection.close()

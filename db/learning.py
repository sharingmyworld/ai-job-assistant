from datetime import datetime

from .connection import get_connection


def create_learning_plan_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_plan (
            id BIGSERIAL PRIMARY KEY,
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

    connection = get_connection()
    cursor = connection.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    for skill in skills:
        clean_skill = str(skill).strip()

        if not clean_skill:
            continue

        cursor.execute(
            """
            INSERT INTO learning_plan
            (
                username,
                skill,
                priority,
                status,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, 'Do nauki', ?, ?)
            ON CONFLICT(username, skill) DO NOTHING
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

    connection = get_connection()
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

    connection = get_connection()
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

    connection = get_connection()
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
    connection = get_connection()
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


def create_roadmap_progress_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roadmap_progress (
            id BIGSERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            skill TEXT NOT NULL,
            step_number INTEGER NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0,
            updated_at TEXT NOT NULL,
            UNIQUE(username, skill, step_number)
        )
    """)

    connection.commit()
    connection.close()


def get_roadmap_progress(username, skill):
    create_roadmap_progress_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT step_number, completed
        FROM roadmap_progress
        WHERE username=? AND skill=?
        """,
        (username, skill)
    )

    rows = cursor.fetchall()
    connection.close()

    return {
        row[0]: bool(row[1])
        for row in rows
    }


def update_roadmap_step(
    username,
    skill,
    step_number,
    completed
):
    create_roadmap_progress_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO roadmap_progress
        (
            username,
            skill,
            step_number,
            completed,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(username, skill, step_number)
        DO UPDATE SET
            completed=excluded.completed,
            updated_at=excluded.updated_at
        """,
        (
            username,
            skill,
            step_number,
            int(completed),
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )
    )

    connection.commit()
    connection.close()


def update_learning_status_by_skill(
    username,
    skill,
    status
):
    allowed_statuses = {
        "Do nauki",
        "W trakcie",
        "Ukończone"
    }

    if status not in allowed_statuses:
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE learning_plan
        SET status=?, updated_at=?
        WHERE username=? AND skill=?
        """,
        (
            status,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            username,
            skill
        )
    )

    connection.commit()
    connection.close()


def create_weekly_goal_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weekly_goals (
            id BIGSERIAL PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            target_steps INTEGER NOT NULL DEFAULT 5,
            start_completed_steps INTEGER NOT NULL DEFAULT 0,
            deadline TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def get_total_completed_roadmap_steps(username):
    create_roadmap_progress_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM roadmap_progress
        WHERE username=? AND completed=1
        """,
        (username,)
    )

    result = cursor.fetchone()
    connection.close()

    return result[0] or 0


def save_weekly_goal(
    username,
    target_steps,
    deadline
):
    create_weekly_goal_table()

    start_completed = (
        get_total_completed_roadmap_steps(username)
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO weekly_goals
        (
            username,
            target_steps,
            start_completed_steps,
            deadline,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(username)
        DO UPDATE SET
            target_steps=excluded.target_steps,
            start_completed_steps=excluded.start_completed_steps,
            deadline=excluded.deadline,
            created_at=excluded.created_at
        """,
        (
            username,
            int(target_steps),
            start_completed,
            deadline,
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )
    )

    connection.commit()
    connection.close()


def get_weekly_goal(username):
    create_weekly_goal_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            target_steps,
            start_completed_steps,
            deadline,
            created_at
        FROM weekly_goals
        WHERE username=?
        """,
        (username,)
    )

    row = cursor.fetchone()
    connection.close()

    return row


def delete_weekly_goal(username):
    create_weekly_goal_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM weekly_goals
        WHERE username=?
        """,
        (username,)
    )

    connection.commit()
    connection.close()

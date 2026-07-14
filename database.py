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

    if "cv_version" not in columns:
        cursor.execute(
            """
            ALTER TABLE analyses
            ADD COLUMN cv_version TEXT DEFAULT ''
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
    missing_skills=None,
    cv_version=""
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



def create_roadmap_progress_table():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS roadmap_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    connection = sqlite3.connect(DATABASE_NAME)
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

    connection = sqlite3.connect(DATABASE_NAME)
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

    connection = sqlite3.connect(DATABASE_NAME)
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
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weekly_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    connection = sqlite3.connect(DATABASE_NAME)
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

    connection = sqlite3.connect(DATABASE_NAME)
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

    connection = sqlite3.connect(DATABASE_NAME)
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

    connection = sqlite3.connect(DATABASE_NAME)
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



def create_job_applications_table():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Planowana',
            application_date TEXT NOT NULL,
            job_url TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            next_event_date TEXT DEFAULT '',
            next_event_type TEXT DEFAULT ''
        )
    """)

    cursor.execute(
        "PRAGMA table_info(job_applications)"
    )

    columns = {
        row[1]
        for row in cursor.fetchall()
    }

    if "match_score" not in columns:
        cursor.execute(
            """
            ALTER TABLE job_applications
            ADD COLUMN match_score REAL
            """
        )


    if "next_event_date" not in columns:
        cursor.execute(
            """
            ALTER TABLE job_applications
            ADD COLUMN next_event_date TEXT DEFAULT ''
            """
        )

    if "next_event_type" not in columns:
        cursor.execute(
            """
            ALTER TABLE job_applications
            ADD COLUMN next_event_type TEXT DEFAULT ''
            """
        )


    if "cv_version" not in columns:
        cursor.execute(
            """
            ALTER TABLE job_applications
            ADD COLUMN cv_version TEXT DEFAULT ''
            """
        )

    connection.commit()
    connection.close()


def add_job_application(
    username,
    company,
    position,
    status,
    application_date,
    job_url="",
    notes="",
    match_score=None,
    next_event_date="",
    next_event_type="",
    cv_version=""
):
    create_job_applications_table()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute(
        """
        INSERT INTO job_applications
        (
            username,
            company,
            position,
            status,
            application_date,
            job_url,
            notes,
            created_at,
            updated_at,
            match_score,
            next_event_date,
            next_event_type,
            cv_version
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            username,
            company.strip(),
            position.strip(),
            status,
            application_date,
            job_url.strip(),
            notes.strip(),
            now,
            now,
            match_score,
            next_event_date,
            next_event_type,
            cv_version.strip()
        )
    )

    connection.commit()
    connection.close()


def get_job_applications(username):
    create_job_applications_table()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            company,
            position,
            status,
            application_date,
            job_url,
            notes,
            created_at,
            updated_at,
            match_score,
            COALESCE(next_event_date, ''),
            COALESCE(next_event_type, ''),
            COALESCE(cv_version, '')
        FROM job_applications
        WHERE username=?
        ORDER BY application_date DESC, id DESC
        """,
        (username,)
    )

    rows = cursor.fetchall()
    connection.close()

    return rows


def update_job_application_status(
    application_id,
    status
):
    allowed_statuses = {
        "Planowana",
        "Wysłana",
        "Rozmowa HR",
        "Rozmowa techniczna",
        "Oferta",
        "Odrzucona",
        "Wycofana"
    }

    if status not in allowed_statuses:
        return

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE job_applications
        SET status=?, updated_at=?
        WHERE id=?
        """,
        (
            status,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            application_id
        )
    )

    connection.commit()
    connection.close()


def update_job_application_notes(
    application_id,
    notes
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE job_applications
        SET notes=?, updated_at=?
        WHERE id=?
        """,
        (
            notes.strip(),
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            application_id
        )
    )

    connection.commit()
    connection.close()


def delete_job_application(application_id):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM job_applications
        WHERE id=?
        """,
        (application_id,)
    )

    connection.commit()
    connection.close()



def update_job_application_event(
    application_id,
    event_date,
    event_type
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE job_applications
        SET
            next_event_date=?,
            next_event_type=?,
            updated_at=?
        WHERE id=?
        """,
        (
            event_date,
            event_type,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            application_id
        )
    )

    connection.commit()
    connection.close()


def get_upcoming_application_events(
    username,
    limit=5
):
    create_job_applications_table()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            company,
            position,
            next_event_date,
            next_event_type,
            status
        FROM job_applications
        WHERE
            username=?
            AND COALESCE(next_event_date, '') != ''
        ORDER BY next_event_date ASC
        LIMIT ?
        """,
        (
            username,
            limit
        )
    )

    rows = cursor.fetchall()
    connection.close()

    return rows



def update_job_application(
    application_id,
    company,
    position,
    application_date,
    job_url,
    match_score=None
):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE job_applications
        SET
            company=?,
            position=?,
            application_date=?,
            job_url=?,
            match_score=?,
            updated_at=?
        WHERE id=?
        """,
        (
            company.strip(),
            position.strip(),
            application_date,
            job_url.strip(),
            match_score,
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            application_id
        )
    )

    connection.commit()
    connection.close()



def get_career_insights_data(username):
    create_database()
    create_learning_plan_table()
    create_job_applications_table()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            score,
            COALESCE(job_title, ''),
            COALESCE(missing_skills, ''),
            COALESCE(cv_version, '')
        FROM analyses
        WHERE username=?
        ORDER BY id DESC
        """,
        (username,)
    )
    analyses = cursor.fetchall()

    cursor.execute(
        """
        SELECT
            skill,
            priority,
            status
        FROM learning_plan
        WHERE username=?
        """,
        (username,)
    )
    learning_plan = cursor.fetchall()

    cursor.execute(
        """
        SELECT
            company,
            position,
            status,
            match_score,
            COALESCE(cv_version, '')
        FROM job_applications
        WHERE username=?
        """,
        (username,)
    )
    applications = cursor.fetchall()

    create_interview_feedback_table()

    cursor.execute(
        """
        SELECT
            interview_type,
            self_rating,
            difficulty,
            result,
            difficult_questions,
            improvements
        FROM interview_feedback
        WHERE username=?
        ORDER BY interview_date DESC, id DESC
        """,
        (username,)
    )
    interview_feedback = cursor.fetchall()

    connection.close()

    return {
        "analyses": analyses,
        "learning_plan": learning_plan,
        "applications": applications,
        "interview_feedback": interview_feedback
    }



def create_interview_prep_table():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_prep (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            application_id INTEGER NOT NULL,
            item_key TEXT NOT NULL,
            item_value TEXT DEFAULT '',
            updated_at TEXT NOT NULL,
            UNIQUE(username, application_id, item_key)
        )
    """)

    connection.commit()
    connection.close()


def save_interview_prep_item(
    username,
    application_id,
    item_key,
    item_value
):
    create_interview_prep_table()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO interview_prep
        (
            username,
            application_id,
            item_key,
            item_value,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(username, application_id, item_key)
        DO UPDATE SET
            item_value=excluded.item_value,
            updated_at=excluded.updated_at
        """,
        (
            username,
            application_id,
            item_key,
            str(item_value),
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )
    )

    connection.commit()
    connection.close()


def get_interview_prep_data(
    username,
    application_id
):
    create_interview_prep_table()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT item_key, item_value
        FROM interview_prep
        WHERE username=? AND application_id=?
        """,
        (
            username,
            application_id
        )
    )

    rows = cursor.fetchall()
    connection.close()

    return {
        key: value
        for key, value in rows
    }



def create_interview_feedback_table():
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            application_id INTEGER NOT NULL,
            interview_date TEXT NOT NULL,
            interview_type TEXT NOT NULL,
            self_rating INTEGER NOT NULL,
            difficulty INTEGER NOT NULL,
            result TEXT NOT NULL,
            difficult_questions TEXT DEFAULT '',
            strengths TEXT DEFAULT '',
            improvements TEXT DEFAULT '',
            next_steps TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            UNIQUE(username, application_id, interview_date, interview_type)
        )
    """)

    connection.commit()
    connection.close()


def save_interview_feedback(
    username,
    application_id,
    interview_date,
    interview_type,
    self_rating,
    difficulty,
    result,
    difficult_questions="",
    strengths="",
    improvements="",
    next_steps=""
):
    create_interview_feedback_table()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    cursor.execute(
        """
        INSERT INTO interview_feedback
        (
            username,
            application_id,
            interview_date,
            interview_type,
            self_rating,
            difficulty,
            result,
            difficult_questions,
            strengths,
            improvements,
            next_steps,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(
            username,
            application_id,
            interview_date,
            interview_type
        )
        DO UPDATE SET
            self_rating=excluded.self_rating,
            difficulty=excluded.difficulty,
            result=excluded.result,
            difficult_questions=excluded.difficult_questions,
            strengths=excluded.strengths,
            improvements=excluded.improvements,
            next_steps=excluded.next_steps,
            updated_at=excluded.updated_at
        """,
        (
            username,
            application_id,
            interview_date,
            interview_type,
            int(self_rating),
            int(difficulty),
            result,
            difficult_questions.strip(),
            strengths.strip(),
            improvements.strip(),
            next_steps.strip(),
            now,
            now
        )
    )

    connection.commit()
    connection.close()


def get_interview_feedback(
    username,
    application_id
):
    create_interview_feedback_table()

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            interview_date,
            interview_type,
            self_rating,
            difficulty,
            result,
            difficult_questions,
            strengths,
            improvements,
            next_steps,
            created_at,
            updated_at
        FROM interview_feedback
        WHERE username=? AND application_id=?
        ORDER BY interview_date DESC, id DESC
        """,
        (
            username,
            application_id
        )
    )

    rows = cursor.fetchall()
    connection.close()

    return rows

from datetime import datetime

from .connection import get_connection


def create_interview_prep_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_prep (
            id BIGSERIAL PRIMARY KEY,
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

    connection = get_connection()
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

    connection = get_connection()
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
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_feedback (
            id BIGSERIAL PRIMARY KEY,
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

    connection = get_connection()
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

    connection = get_connection()
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


def create_mock_interview_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mock_interview_answers (
            id BIGSERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            application_id INTEGER NOT NULL,
            question_number INTEGER NOT NULL,
            question TEXT NOT NULL,
            answer TEXT DEFAULT '',
            score INTEGER NOT NULL DEFAULT 0,
            feedback TEXT DEFAULT '',
            updated_at TEXT NOT NULL,
            UNIQUE(username, application_id, question_number)
        )
    """)

    cursor.execute(
        "ALTER TABLE mock_interview_answers "
        "ADD COLUMN IF NOT EXISTS feedback TEXT DEFAULT ''"
    )

    connection.commit()
    connection.close()


def save_mock_interview_answer(
    username,
    application_id,
    question_number,
    question,
    answer,
    score,
    feedback=""
):
    create_mock_interview_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO mock_interview_answers
        (
            username,
            application_id,
            question_number,
            question,
            answer,
            score,
            feedback,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(
            username,
            application_id,
            question_number
        )
        DO UPDATE SET
            question=excluded.question,
            answer=excluded.answer,
            score=excluded.score,
            feedback=excluded.feedback,
            updated_at=excluded.updated_at
        """,
        (
            username,
            application_id,
            question_number,
            question,
            answer.strip(),
            int(score),
            feedback.strip(),
            datetime.now().strftime("%Y-%m-%d %H:%M")
        )
    )

    connection.commit()
    connection.close()


def get_mock_interview_answers(
    username,
    application_id
):
    create_mock_interview_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            question_number,
            question,
            answer,
            score,
            COALESCE(feedback, '')
        FROM mock_interview_answers
        WHERE username=? AND application_id=?
        ORDER BY question_number
        """,
        (
            username,
            application_id
        )
    )

    rows = cursor.fetchall()
    connection.close()

    return {
        row[0]: {
            "question": row[1],
            "answer": row[2],
            "score": row[3],
            "feedback": row[4]
        }
        for row in rows
    }


def reset_mock_interview(
    username,
    application_id
):
    create_mock_interview_table()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM mock_interview_answers
        WHERE username=? AND application_id=?
        """,
        (
            username,
            application_id
        )
    )

    connection.commit()
    connection.close()

from .connection import get_connection


def delete_user_account(username):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        tables = [
            "mock_interview_answers",
            "interview_feedback",
            "interview_prep",
            "job_applications",
            "weekly_goals",
            "roadmap_progress",
            "learning_plan",
            "analyses",
            "remember_tokens",
        ]

        for table in tables:
            cursor.execute(
                f"DELETE FROM {table} WHERE username=?",
                (username,),
            )

        cursor.execute(
            "DELETE FROM users WHERE username=?",
            (username,),
        )

        if cursor.rowcount != 1:
            raise RuntimeError("Nie znaleziono konta.")

        connection.commit()
        return True
    except Exception:
        connection._connection.rollback()
        raise
    finally:
        connection.close()

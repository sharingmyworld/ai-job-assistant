from .connection import get_connection
from .analyses import create_database
from .learning import create_learning_plan_table
from .applications import create_job_applications_table
from .interviews import (
    create_interview_feedback_table,
    create_mock_interview_table,
)


def get_career_insights_data(username):
    create_database()
    create_learning_plan_table()
    create_job_applications_table()

    connection = get_connection()
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

    create_mock_interview_table()

    cursor.execute(
        """
        SELECT
            application_id,
            question_number,
            question,
            answer,
            score,
            updated_at
        FROM mock_interview_answers
        WHERE username=?
        ORDER BY updated_at ASC, question_number ASC
        """,
        (username,)
    )
    mock_interview_answers = cursor.fetchall()

    connection.close()

    return {
        "analyses": analyses,
        "learning_plan": learning_plan,
        "applications": applications,
        "interview_feedback": interview_feedback,
        "mock_interview_answers": mock_interview_answers
    }

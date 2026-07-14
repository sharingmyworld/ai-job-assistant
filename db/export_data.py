from datetime import datetime

from .connection import get_connection


def _fetch_rows(cursor, query, params, columns):
    cursor.execute(query, params)

    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def export_user_data(username):
    connection = get_connection()
    cursor = connection.cursor()

    try:
        analyses = _fetch_rows(
            cursor,
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
            ORDER BY id
            """,
            (username,),
            [
                "id",
                "date",
                "score",
                "skills",
                "job_title",
                "missing_skills",
                "cv_version",
            ],
        )

        learning_plan = _fetch_rows(
            cursor,
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
            ORDER BY id
            """,
            (username,),
            [
                "id",
                "skill",
                "priority",
                "status",
                "created_at",
                "updated_at",
            ],
        )

        roadmap_progress = _fetch_rows(
            cursor,
            """
            SELECT
                id,
                skill,
                step_number,
                completed,
                updated_at
            FROM roadmap_progress
            WHERE username=?
            ORDER BY skill, step_number
            """,
            (username,),
            [
                "id",
                "skill",
                "step_number",
                "completed",
                "updated_at",
            ],
        )

        weekly_goals = _fetch_rows(
            cursor,
            """
            SELECT
                id,
                target_steps,
                start_completed_steps,
                deadline,
                created_at
            FROM weekly_goals
            WHERE username=?
            ORDER BY id
            """,
            (username,),
            [
                "id",
                "target_steps",
                "start_completed_steps",
                "deadline",
                "created_at",
            ],
        )

        applications = _fetch_rows(
            cursor,
            """
            SELECT
                id,
                company,
                position,
                status,
                application_date,
                COALESCE(job_url, ''),
                COALESCE(notes, ''),
                created_at,
                updated_at,
                match_score,
                COALESCE(next_event_date, ''),
                COALESCE(next_event_type, ''),
                COALESCE(cv_version, '')
            FROM job_applications
            WHERE username=?
            ORDER BY id
            """,
            (username,),
            [
                "id",
                "company",
                "position",
                "status",
                "application_date",
                "job_url",
                "notes",
                "created_at",
                "updated_at",
                "match_score",
                "next_event_date",
                "next_event_type",
                "cv_version",
            ],
        )

        interview_prep = _fetch_rows(
            cursor,
            """
            SELECT
                id,
                application_id,
                item_key,
                item_value,
                updated_at
            FROM interview_prep
            WHERE username=?
            ORDER BY application_id, item_key
            """,
            (username,),
            [
                "id",
                "application_id",
                "item_key",
                "item_value",
                "updated_at",
            ],
        )

        interview_feedback = _fetch_rows(
            cursor,
            """
            SELECT
                id,
                application_id,
                interview_date,
                interview_type,
                self_rating,
                difficulty,
                result,
                COALESCE(difficult_questions, ''),
                COALESCE(strengths, ''),
                COALESCE(improvements, ''),
                COALESCE(next_steps, ''),
                created_at,
                updated_at
            FROM interview_feedback
            WHERE username=?
            ORDER BY id
            """,
            (username,),
            [
                "id",
                "application_id",
                "interview_date",
                "interview_type",
                "self_rating",
                "difficulty",
                "result",
                "difficult_questions",
                "strengths",
                "improvements",
                "next_steps",
                "created_at",
                "updated_at",
            ],
        )

        mock_interview = _fetch_rows(
            cursor,
            """
            SELECT
                id,
                application_id,
                question_number,
                question,
                answer,
                score,
                COALESCE(feedback, ''),
                updated_at
            FROM mock_interview_answers
            WHERE username=?
            ORDER BY application_id, question_number
            """,
            (username,),
            [
                "id",
                "application_id",
                "question_number",
                "question",
                "answer",
                "score",
                "feedback",
                "updated_at",
            ],
        )
    finally:
        connection.close()

    return {
        "export_version": 1,
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "username": username,
        "data": {
            "analyses": analyses,
            "learning_plan": learning_plan,
            "roadmap_progress": roadmap_progress,
            "weekly_goals": weekly_goals,
            "job_applications": applications,
            "interview_prep": interview_prep,
            "interview_feedback": interview_feedback,
            "mock_interview_answers": mock_interview,
        },
    }

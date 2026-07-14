from datetime import datetime

from .connection import get_connection


def create_job_applications_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_applications (
            id BIGSERIAL PRIMARY KEY,
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
        "ALTER TABLE job_applications "
        "ADD COLUMN IF NOT EXISTS match_score REAL"
    )
    cursor.execute(
        "ALTER TABLE job_applications "
        "ADD COLUMN IF NOT EXISTS next_event_date TEXT DEFAULT ''"
    )
    cursor.execute(
        "ALTER TABLE job_applications "
        "ADD COLUMN IF NOT EXISTS next_event_type TEXT DEFAULT ''"
    )
    cursor.execute(
        "ALTER TABLE job_applications "
        "ADD COLUMN IF NOT EXISTS cv_version TEXT DEFAULT ''"
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

    connection = get_connection()
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

    connection = get_connection()
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

    connection = get_connection()
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
    connection = get_connection()
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
    connection = get_connection()
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
    connection = get_connection()
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

    connection = get_connection()
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
    connection = get_connection()
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

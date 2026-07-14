from datetime import datetime

from .connection import get_connection


def create_remember_tokens_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS remember_tokens (
            id BIGSERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            token_hash TEXT NOT NULL UNIQUE,
            expires_at TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def create_remember_token(username, days=30):
    import hashlib
    import secrets
    from datetime import timedelta

    create_remember_tokens_table()

    raw_token = secrets.token_urlsafe(48)
    token_hash = hashlib.sha256(
        raw_token.encode("utf-8")
    ).hexdigest()

    now = datetime.now()
    expires_at = now + timedelta(days=days)

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM remember_tokens
        WHERE username=? OR expires_at < ?
        """,
        (
            username,
            now.strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    cursor.execute(
        """
        INSERT INTO remember_tokens
        (
            username,
            token_hash,
            expires_at,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            username,
            token_hash,
            expires_at.strftime("%Y-%m-%d %H:%M:%S"),
            now.strftime("%Y-%m-%d %H:%M:%S")
        )
    )

    connection.commit()
    connection.close()

    return raw_token


def validate_remember_token(raw_token):
    import hashlib

    if not raw_token:
        return None

    create_remember_tokens_table()

    token_hash = hashlib.sha256(
        raw_token.encode("utf-8")
    ).hexdigest()

    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT username
        FROM remember_tokens
        WHERE token_hash=? AND expires_at >= ?
        """,
        (
            token_hash,
            now
        )
    )

    row = cursor.fetchone()
    connection.close()

    return row[0] if row else None


def revoke_remember_token(raw_token):
    import hashlib

    if not raw_token:
        return

    create_remember_tokens_table()

    token_hash = hashlib.sha256(
        raw_token.encode("utf-8")
    ).hexdigest()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM remember_tokens
        WHERE token_hash=?
        """,
        (token_hash,)
    )

    connection.commit()
    connection.close()

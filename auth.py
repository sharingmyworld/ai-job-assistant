import bcrypt
import psycopg2

from database import get_connection


def create_users_table():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id BIGSERIAL PRIMARY KEY,

            username TEXT UNIQUE,

            password TEXT

        )
    """)

    connection.commit()
    connection.close()


def register_user(username, password):

    connection = get_connection()
    cursor = connection.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    try:

        cursor.execute(

            """
            INSERT INTO users(username, password)
            VALUES (?, ?)
            """,

            (
                username,
                hashed_password
            )

        )

        connection.commit()

        success = True

    except psycopg2.IntegrityError:

        success = False

    connection.close()

    return success


def login_user(username, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(

        """
        SELECT password
        FROM users
        WHERE username=?
        """,

        (
            username,
        )

    )

    row = cursor.fetchone()

    connection.close()

    if row is None:

        return False

    return bcrypt.checkpw(

        password.encode(),

        row[0]

    )


def change_password(username, current_password, new_password):

    if not login_user(
        username,
        current_password
    ):
        return False, "Obecne hasło jest nieprawidłowe."

    hashed_password = bcrypt.hashpw(
        new_password.encode("utf-8"),
        bcrypt.gensalt()
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET password=?
        WHERE username=?
        """,
        (
            hashed_password,
            username
        )
    )

    connection.commit()

    updated_rows = cursor.rowcount

    connection.close()

    if updated_rows == 0:
        return False, "Nie znaleziono użytkownika."

    return True, "Hasło zostało zmienione."
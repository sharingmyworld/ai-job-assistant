import sqlite3
import bcrypt


DATABASE_NAME = "history.db"


def create_users_table():

    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE,

            password TEXT

        )
    """)

    connection.commit()
    connection.close()


def register_user(username, password):

    connection = sqlite3.connect(DATABASE_NAME)
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

    except sqlite3.IntegrityError:

        success = False

    connection.close()

    return success


def login_user(username, password):

    connection = sqlite3.connect(DATABASE_NAME)
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

    connection = sqlite3.connect(DATABASE_NAME)
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
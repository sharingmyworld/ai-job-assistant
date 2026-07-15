import os
import re
from datetime import datetime
from threading import Lock

import psycopg2
from psycopg2 import OperationalError, InterfaceError
from psycopg2.pool import ThreadedConnectionPool


DATABASE_URL = os.environ.get("DATABASE_URL")


class DatabaseUnavailableError(RuntimeError):
    """Raised when PostgreSQL is temporarily unavailable."""

_pool = None
_pool_lock = Lock()


def _get_pool():
    global _pool

    if not DATABASE_URL:
        raise RuntimeError(
            "Brak zmiennej DATABASE_URL."
        )

    if _pool is None:
        with _pool_lock:
            if _pool is None:
                _pool = ThreadedConnectionPool(
                    minconn=1,
                    maxconn=5,
                    dsn=DATABASE_URL,
                    connect_timeout=10,
                    keepalives=1,
                    keepalives_idle=30,
                    keepalives_interval=10,
                    keepalives_count=3,
                )

    return _pool


class DatabaseCursor:
    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, query, params=None):
        query = re.sub(r"\?", "%s", query)
        self._cursor.execute(query, params)
        return self

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def close(self):
        self._cursor.close()

    @property
    def rowcount(self):
        return self._cursor.rowcount


class DatabaseConnection:
    def __init__(self):
        self._pool = _get_pool()
        self._connection = self._pool.getconn()
        self._cursors = []

    def cursor(self):
        cursor = DatabaseCursor(
            self._connection.cursor()
        )
        self._cursors.append(cursor)
        return cursor

    def commit(self):
        self._connection.commit()

    def close(self):
        for cursor in self._cursors:
            try:
                cursor.close()
            except Exception:
                pass

        self._cursors.clear()

        try:
            self._connection.rollback()
        except Exception:
            pass

        self._pool.putconn(
            self._connection
        )


def get_connection():
    last_error = None

    for _ in range(2):
        try:
            return DatabaseConnection()
        except (OperationalError, InterfaceError) as error:
            last_error = error
            reset_connection_pool()

    raise DatabaseUnavailableError(
        "Baza danych jest chwilowo niedostępna."
    ) from last_error


def reset_connection_pool():
    global _pool

    with _pool_lock:
        if _pool is not None:
            try:
                _pool.closeall()
            except Exception:
                pass

            _pool = None

import os
import oracledb


def get_connection():
    """Connect to the Oracle database."""
    username = os.getenv("DB_USER", "system")
    password = os.getenv("DB_PASSWORD", "")
    dsn = os.getenv("DB_DSN", "localhost:1521/XE")

    if not password:
        raise RuntimeError(
            "DB_PASSWORD set nahi hai. Apna Oracle password configure karo."
        )

    return oracledb.connect(
        user=username,
        password=password,
        dsn=dsn
    )


def test_connection():
    """Test whether Oracle is reachable."""
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT SYSDATE FROM dual")
            return cursor.fetchone()[0]
    finally:
        connection.close()
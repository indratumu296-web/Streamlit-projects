import streamlit as st
import psycopg2
from contextlib import contextmanager
from psycopg2.extras import RealDictCursor


@contextmanager
def get_connection():
    conn = None
    try:
        pg_config = st.secrets.get("postgres", {})

        if "url" in pg_config:
            conn = psycopg2.connect(pg_config["url"], cursor_factory=RealDictCursor)
        else:
            missing = [
                key for key in ("host", "port", "database", "user", "password")
                if key not in pg_config or pg_config[key] in (None, "")
            ]
            if missing:
                raise ValueError(
                    "Missing PostgreSQL secrets: " + ", ".join(missing) + ". "
                    "Add them under [postgres] in .streamlit/secrets.toml."
                )

            conn = psycopg2.connect(
                host=pg_config["host"],
                port=pg_config["port"],
                database=pg_config["database"],
                user=pg_config["user"],
                password=pg_config["password"],
                cursor_factory=RealDictCursor,
            )

        yield conn
        conn.commit()
    finally:
        if conn is not None:
            conn.close()


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )


def create_user(username, email, password_hash):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                    (username, email, password_hash),
                )
        return True
    except psycopg2.errors.UniqueViolation:
        return False


def get_user_by_username(username):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            return cur.fetchone()


def get_all_users():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, email, created_at FROM users ORDER BY id")
            return cur.fetchall()


def user_exists(username=None, email=None):
    if username is None and email is None:
        return False

    with get_connection() as conn:
        with conn.cursor() as cur:
            if username is not None:
                cur.execute("SELECT 1 FROM users WHERE username = %s", (username,))
            elif email is not None:
                cur.execute("SELECT 1 FROM users WHERE email = %s", (email,))
            return cur.fetchone() is not None

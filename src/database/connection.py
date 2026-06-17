import sqlite3
from pathlib import Path


DB_PATH = Path("data/reviews.db")
SCHEMA_PATH = Path("src/database/schema.sql")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    with get_connection() as conn:
        schema_sql = SCHEMA_PATH.read_text()
        conn.executescript(schema_sql)
        conn.commit()

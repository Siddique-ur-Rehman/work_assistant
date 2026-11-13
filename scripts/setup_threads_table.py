
import psycopg
from app.config.settings import settings

SQL = """
CREATE TABLE IF NOT EXISTS threads (
    thread_id  TEXT PRIMARY KEY,
    user_id    TEXT NOT NULL,
    title      TEXT NOT NULL DEFAULT 'New chat',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS threads_user_idx ON threads (user_id);
"""

with psycopg.connect(settings.app_db_url, autocommit=True) as conn:
    conn.execute(SQL)
    print("threads table is ready")
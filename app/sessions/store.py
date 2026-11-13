
import uuid

from app.sessions.db import pool


def create_thread(user_id):
    thread_id = str(uuid.uuid4())
    with pool.connection() as conn:
        conn.execute(
            "INSERT INTO threads (thread_id, user_id) VALUES (%s, %s)",
            (thread_id, user_id),
        )
    return thread_id


def list_threads(user_id):
    with pool.connection() as conn:
        return conn.execute(
            "SELECT thread_id, title, created_at, updated_at FROM threads "
            "WHERE user_id = %s ORDER BY updated_at DESC",
            (user_id,),
        ).fetchall()


def get_thread(thread_id, user_id):
    """Returns the thread only if it belongs to this user, otherwise None."""
    with pool.connection() as conn:
        return conn.execute(
            "SELECT thread_id, title FROM threads WHERE thread_id = %s AND user_id = %s",
            (thread_id, user_id),
        ).fetchone()


def rename_thread(thread_id, user_id, title):
    with pool.connection() as conn:
        conn.execute(
            "UPDATE threads SET title = %s, updated_at = now() "
            "WHERE thread_id = %s AND user_id = %s",
            (title, thread_id, user_id),
        )


def touch_thread(thread_id):
    with pool.connection() as conn:
        conn.execute("UPDATE threads SET updated_at = now() WHERE thread_id = %s", (thread_id,))


def delete_thread_row(thread_id, user_id):
    with pool.connection() as conn:
        conn.execute(
            "DELETE FROM threads WHERE thread_id = %s AND user_id = %s",
            (thread_id, user_id),
        )
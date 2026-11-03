# Goal: prove we can connect to local Postgres.
import psycopg
from app.config.settings import settings

# Open a connection using the URL from .env
with psycopg.connect(settings.app_db_url) as conn:
    # Ask Postgres for its version, a simple "are you alive?" check
    result = conn.execute("SELECT version()").fetchone()
    print("Postgres is working:", result[0])
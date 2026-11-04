
import psycopg
from app.config.settings import settings


with psycopg.connect(settings.app_db_url) as conn:
    
    result = conn.execute("SELECT version()").fetchone()
    print("Postgres is working:", result[0])
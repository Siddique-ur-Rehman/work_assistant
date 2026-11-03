# Reads your .env file and makes the values easy to use everywhere.
import os
from dotenv import load_dotenv

# Load the values from the .env file into the environment
load_dotenv()


def get_value(name):
    """Get one value from .env. Stop with a clear message if it's missing."""
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing {name} in your .env file")
    return value


class Settings:
    def __init__(self):
        # Only the Postgres URL for now. We add more as we need them.
        self.app_db_url = get_value("APP_DB_URL")


# Create it once. Other files import it like this:
# from app.config.settings import settings
settings = Settings()
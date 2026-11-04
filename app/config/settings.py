
import os
from dotenv import load_dotenv


load_dotenv()


def get_value(name):
    """Get one value from .env. Stop with a clear message if it's missing."""
    value = os.getenv(name)
    if not value:
        raise ValueError(f"Missing {name} in your .env file")
    return value


class Settings:
    def __init__(self):
        
        self.app_db_url = get_value("APP_DB_URL")
                
        self.qdrant_url = get_value("QDRANT_URL")
        self.qdrant_api_key = get_value("QDRANT_API_KEY")



settings = Settings()
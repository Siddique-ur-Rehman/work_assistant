
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from app.config.settings import settings


pool = ConnectionPool(
    settings.app_db_url,
    min_size=1,
    max_size=5,
    kwargs={"autocommit": True, "row_factory": dict_row},
    open=False,   
)
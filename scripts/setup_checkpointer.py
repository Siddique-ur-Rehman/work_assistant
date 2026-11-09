
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.store.postgres import PostgresStore
from app.config.settings import settings

# Create the conversation (checkpoint) tables
with PostgresSaver.from_conn_string(settings.app_db_url) as checkpointer:
    checkpointer.setup()  # safe to run again, it won't duplicate tables
    print("Checkpoint tables are ready")

# Create the long-term memory (store) tables
with PostgresStore.from_conn_string(settings.app_db_url) as store:
    store.setup()
    print("Memory store tables are ready")
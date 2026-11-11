
import sys

from langgraph.checkpoint.postgres import PostgresSaver

from app.config.settings import settings
from app.graph.nodes.builder import build_graph

thread_id = sys.argv[1]
question = sys.argv[2]


with PostgresSaver.from_conn_string(settings.app_db_url) as checkpointer:
    app = build_graph(checkpointer)

  
    config = {"configurable": {"thread_id": thread_id}}
    result = app.invoke({"question": question}, config)

    print("ANSWER:\n", result["answer"])
    print("\nMessages saved in this thread:", len(result["messages"]))
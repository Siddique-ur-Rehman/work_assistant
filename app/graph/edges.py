

from app.config.settings import settings
def route_after_router(state):
    if state["intent"] == "search":
        return "retrieve"
    if state["intent"] == "history":
        return "chat_history"
    return "out_of_scope"

def route_after_grade(state):
    if state["grade"] == "good":
        return "answer"
    # Weak results: retry only while we are under the limit
    if state.get("retry_count", 0) < settings.max_retrieval_retries:
        return "retry_query"
    return "no_answer"
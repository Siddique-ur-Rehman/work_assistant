
def route_after_router(state):
    if state["intent"] == "search":
        return "retrieve"
    if state["intent"] == "history":
        return "chat_history"
    return "out_of_scope"
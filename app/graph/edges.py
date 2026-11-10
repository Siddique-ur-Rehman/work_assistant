
def route_after_router(state):
    if state["collections"]:
        return "retrieve"      
    return "out_of_scope"       
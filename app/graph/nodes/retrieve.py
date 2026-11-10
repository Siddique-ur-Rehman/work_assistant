
from app.rag.retriever import search_all


def retrieve_node(state):
    documents = search_all(state["question"])
    # A node returns only the fields it wants to update
    return {"documents": documents}
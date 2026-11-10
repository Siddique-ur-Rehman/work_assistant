
from app.rag.retriever import search_collections


def retrieve_node(state):
    documents = search_collections(state["question"], state["collections"])
    return {"documents": documents}
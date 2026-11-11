from app.rag.retriever import search_collections


def retrieve_node(state):
    documents = search_collections(state["search_query"], state["collections"])
    return {"documents": documents}
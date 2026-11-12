from app.rag.retriever import search_collections


def retrieve_node(state):
    try:
        documents = search_collections(state["search_query"], state["collections"])
    except Exception as error:
        print(f"[retrieval failed] {type(error).__name__}: {error}")
        documents = []
    return {"documents": documents}
# Searches the Qdrant collections and returns simple dictionaries.
from langchain_qdrant import QdrantVectorStore
from app.config.settings import settings
from app.rag.embedding import get_embeddings

COLLECTIONS = ["licensing_regulations", "health_policy_kpk"]

embeddings = get_embeddings()
_stores = {}  # keeps opened collections so we don't reconnect every time


def get_store(name):
    if name not in _stores:
        _stores[name] = QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            collection_name=name,
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
    return _stores[name]


def search_all(question, k=3):
    """Search every collection and return the best chunks, highest score first."""
    found = []
    for name in COLLECTIONS:
        results = get_store(name).similarity_search_with_score(question, k=k)
        for doc, score in results:
            found.append({
                "text": doc.page_content,
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page"),
                "collection": name,
                "score": score,
            })
    found.sort(key=lambda item: item["score"], reverse=True)
    return found[:k * 2]
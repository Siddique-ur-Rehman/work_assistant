
from langchain_qdrant import QdrantVectorStore
from app.config.settings import settings
from app.rag.embedding import get_embeddings

embeddings = get_embeddings()
_stores = {}  


def get_store(name):
    if name not in _stores:
        _stores[name] = QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            collection_name=name,
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
    return _stores[name]


def search_collections(question, collections, k=3):
    """Search only the given collections, best chunks first."""
    found = []
    for name in collections:
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
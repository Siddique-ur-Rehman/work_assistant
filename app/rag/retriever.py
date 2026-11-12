
from langchain_qdrant import FastEmbedSparse, QdrantVectorStore, RetrievalMode

from app.config.settings import settings
from app.rag.embedding import get_embeddings
from app.rag.reranker import rerank

embeddings = get_embeddings()
sparse_embeddings = FastEmbedSparse(model_name="Qdrant/bm25")
_stores = {}  


def get_store(name):
    if name not in _stores:
        _stores[name] = QdrantVectorStore.from_existing_collection(
            embedding=embeddings,
            sparse_embedding=sparse_embeddings,
            retrieval_mode=RetrievalMode.HYBRID,
            collection_name=name,
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
    return _stores[name]


def search_collections(question, collections, fetch_k=10, top_n=5):
    """Hybrid-search each collection, then rerank everything and keep the best."""
    candidates = []
    for name in collections:
        docs = get_store(name).similarity_search(question, k=fetch_k)
        for doc in docs:
            candidates.append({
                "text": doc.page_content,
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page"),
                "collection": name,
                "score": 0.0,
            })
    return rerank(question, candidates, top_n=top_n)
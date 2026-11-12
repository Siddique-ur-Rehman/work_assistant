# Goal: ask one question and search BOTH collections.
from langchain_qdrant import QdrantVectorStore
from app.config.settings import settings
from app.rag.embedding import get_embeddings

embeddings = get_embeddings()

QUESTION = "What was mission of kpk health department?"

COLLECTIONS = ["licensing_regulations", "health_policy_kpk"]

for name in COLLECTIONS:
    store = QdrantVectorStore.from_existing_collection(
        embedding=embeddings,
        collection_name=name,
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
    )
    results = store.similarity_search_with_score(QUESTION, k=3)

    print(f"\n===== {name} =====")
    for i, (doc, score) in enumerate(results, start=1):
        print(f"\n--- Result {i} | score {score:.3f} ---")
        print(f"File: {doc.metadata.get('source')} | Page: {doc.metadata.get('page')}")
        print(doc.page_content[:300])

from app.rag.retriever import search_collections

QUESTION = "How safe blood transfusion will be provided to KPK people?"
COLLECTIONS = ["licensing_regulations", "health_policy_kpk"]

results = search_collections(QUESTION, COLLECTIONS)

for i, r in enumerate(results, start=1):
    print(f"\n--- Result {i} | rerank score {r['score']:.2f} | {r['collection']} ---")
    print(f"File: {r['source']} | Page: {r['page']}")
    print(r["text"][:300])
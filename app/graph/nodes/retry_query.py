
from app.config.collection import COLLECTIONS
from app.rag.llm import get_llm

PROMPT = """The search for this question returned weak results.
Write a better search query: use different keywords or synonyms, keep the same meaning.
Return ONLY the new query.

Question: {question}
Previous query: {query}
New query:"""


def retry_query_node(state):
    prompt = PROMPT.format(
        question=state["standalone_question"], query=state["search_query"]
    )
    new_query = get_llm().invoke(prompt).content.strip()
    count = state.get("retry_count", 0) + 1

    print(f"[retry {count}] new query: '{new_query}' (searching all collections)")
    return {
        "search_query": new_query,
        "retry_count": count,
        "collections": list(COLLECTIONS),   
    }
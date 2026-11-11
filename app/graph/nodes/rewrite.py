
from app.rag.llm import get_llm

REWRITE_PROMPT = """Rewrite the user's latest question so it makes sense on its own.
Use the conversation to replace words like "it", "that", "they".
If the question is about the conversation itself (e.g. "what did I ask before?"), return it unchanged.
If it already makes sense on its own, return it unchanged.
Return ONLY the question, nothing else.

Conversation:
{history}

Latest question: {question}
Standalone question:"""


def rewrite_node(state):
    messages = state.get("messages", [])

    if not messages:
        standalone = state["question"]         
    else:
        history = "\n".join(f"{m.type}: {m.content}" for m in messages[-6:])
        prompt = REWRITE_PROMPT.format(history=history, question=state["question"])
        standalone = get_llm().invoke(prompt).content.strip()
        print(f"[rewrite] '{state['question']}' -> '{standalone}'")

    
    return {
        "standalone_question": standalone,
        "search_query": standalone,
        "retry_count": 0,
        "grade": "",
    }
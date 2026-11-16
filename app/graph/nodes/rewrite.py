
from app.rag.llm import ask_llm

REFERENCE_WORDS = {
    "it", "its", "that", "this", "they", "them", "their", "those", "these",
    "he", "she", "his", "her", "previous", "above", "earlier", "same",
    "also", "too", "another",
}

REWRITE_PROMPT = """Rewrite the user's latest question so it makes sense on its own.
Only replace words like "it", "that", "they" using the conversation.
Do NOT add any new topic, document name, organization, or detail.
Keep the wording as close as possible to the original.
Return ONLY the question.

Conversation:
{history}

Latest question: {question}
Standalone question:"""


def needs_rewrite(question):
    words = [w.strip("?.,!").lower() for w in question.split()]
    short = len(words) <= 4                       # "what about fees?"
    refers_back = any(w in REFERENCE_WORDS for w in words)
    return short or refers_back


def rewrite_node(state):
    messages = state.get("messages", [])
    question = state["question"]
    standalone = question

   
    if messages and needs_rewrite(question):
        history = "\n".join(f"{m.type}: {m.content}" for m in messages[-6:])
        standalone = ask_llm(
            REWRITE_PROMPT.format(history=history, question=question), question
        )
        print(f"[rewrite] '{question}' -> '{standalone}'")
    else:
        print("[rewrite] skipped (question is already clear)")

    
    return {
        "standalone_question": standalone,
        "search_query": standalone,
        "retry_count": 0,
        "grade": "",
    }
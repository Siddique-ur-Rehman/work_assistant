# Node: answer questions about the conversation itself.
from app.rag.llm import get_llm

PROMPT = """Answer the user's question using ONLY the conversation below.

Conversation:
{history}

Question: {question}
"""


def chat_history_node(state):
    messages = state.get("messages", [])
    if not messages:
        answer = "We haven't talked about anything yet in this conversation."
    else:
        history = "\n".join(f"{m.type}: {m.content}" for m in messages[-10:])
        answer = get_llm().invoke(
            PROMPT.format(history=history, question=state["question"])
        ).content

    return {
        "documents": [],
        "answer": answer,
        "messages": [("user", state["question"]), ("assistant", answer)],
    }
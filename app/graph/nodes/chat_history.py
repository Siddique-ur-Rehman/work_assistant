# Node: answer questions about the conversation itself.
from app.rag.llm import ask_llm

PROMPT = """Answer the user's question using ONLY the conversation below.
Lines starting with "human" are the user's earlier questions.

Conversation:
{history}

Question: {question}
Answer:"""


def chat_history_node(state):
    messages = state.get("messages", [])

    if not messages:
        answer = "We haven't talked about anything yet in this conversation."
    else:
        recent = messages[-10:]
        history = "\n".join(f"{m.type}: {m.content}" for m in recent)
        print(f"[history] sending {len(recent)} messages")

       
        prompt = PROMPT.format(history=history, question=state["question"])
        answer = ask_llm(
            prompt,
            "The assistant is temporarily unavailable. Please try again shortly.",
        )

    return {
        "documents": [],
        "answer": answer,
        "messages": [("user", state["question"]), ("assistant", answer)],
    }
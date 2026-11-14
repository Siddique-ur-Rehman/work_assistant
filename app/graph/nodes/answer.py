
from app.rag.llm import ask_llm

PROMPT = """You are a healthcare policy assistant.
Answer the question using ONLY the context below.
After each fact, cite the source like (file name, page).
If the context does not contain the answer, say exactly: "I don't know based on the available documents."
What we know about the user (use ONLY to adjust style and relevance.
Never use it as a source of facts):
{memories}

Recent conversation:
{history}

Context:
{context}

Question: {question}
"""


def answer_node(state):
  
    history = "\n".join(
        f"{m.type}: {m.content}" for m in state.get("messages", [])[-6:]
    ) or "(none)"

    context = "\n\n".join(
        f"[{d['source']}, page {d['page']}]\n{d['text']}"
        for d in state["documents"]
    )
    memories = "\n".join(f"- {m}" for m in state.get("memories", [])) or "(none)"

    prompt = PROMPT.format(memories=memories,history=history, context=context, question=state["standalone_question"])
    answer = ask_llm(prompt, "The assistant is temporarily unavailable. Please try again shortly.")

    
    return {
        "answer": answer,
        "messages": [("user", state["question"]), ("assistant", answer)],
    }
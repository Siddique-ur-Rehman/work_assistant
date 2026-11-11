
from app.rag.llm import get_llm

GRADE_PROMPT = """You check search results.

Question: {question}

Search results:
{context}

Do these results contain at least PART of the information needed to answer the question?
Reply yes if they are clearly on the right topic and contain relevant facts, even if the answer is incomplete.
Reply no only if they are off-topic or contain nothing useful.
Reply with ONE word only: yes or no."""


def grade_node(state):
    documents = state.get("documents", [])

    
    if not documents:
        print("[grade] no documents -> weak")
        return {"grade": "weak"}

    context = "\n\n".join(d["text"] for d in documents[:4])
    prompt = GRADE_PROMPT.format(question=state["standalone_question"], context=context)
    reply = get_llm().invoke(prompt).content.strip().lower()

    grade = "good" if reply.startswith("yes") else "weak"
    print(f"[grade] reply='{reply}' -> {grade}")
    return {"grade": grade}
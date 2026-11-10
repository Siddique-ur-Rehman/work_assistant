
from app.rag.llm import get_llm

PROMPT = """You are a healthcare policy assistant.
Answer the question using ONLY the context below.
After each fact, cite the source like (file name, page).
If the context does not contain the answer, say exactly: "I don't know based on the available documents."

Context:
{context}

Question: {question}
"""


def answer_node(state):
    # Turn the chunks into one text block, with a label on each
    context = "\n\n".join(
        f"[{d['source']}, page {d['page']}]\n{d['text']}"
        for d in state["documents"]
    )
    prompt = PROMPT.format(context=context, question=state["question"])
    response = get_llm().invoke(prompt)
    return {"answer": response.content}
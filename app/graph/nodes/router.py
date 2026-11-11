# Node: decide what to do with the question.
from app.config.collection import COLLECTIONS
from app.rag.llm import get_llm

ROUTER_PROMPT = """You route questions.

Collections:
{descriptions}

Reply with ONE of these words only:
{options}

- Use "both" if the question needs both collections.
- Use "history" if the question is about the conversation itself
  (for example: "what did I ask before?", "summarize our chat").
- Use "none" if it is not about healthcare licensing or KP health policy.

Question: {question}
Answer:"""


def router_node(state):
    descriptions = "\n".join(f"- {name}: {text}" for name, text in COLLECTIONS.items())
    options = ", ".join(list(COLLECTIONS) + ["both", "history", "none"])
    question = state["standalone_question"]

    prompt = ROUTER_PROMPT.format(
        descriptions=descriptions, options=options, question=question
    )
    reply = get_llm().invoke(prompt).content.strip().lower()

    if "history" in reply:
        intent, chosen = "history", []
    elif "none" in reply:
        intent, chosen = "none", []
    else:
        intent = "search"
        chosen = [name for name in COLLECTIONS if name in reply]
        if not chosen:                      # "both" or unclear: search all
            chosen = list(COLLECTIONS)

    print(f"[router] reply='{reply}' -> intent={intent}, collections={chosen}")
    return {"intent": intent, "collections": chosen}
# Node: decide which collection(s) should be searched.
from app.config.collection import COLLECTIONS
from app.rag.llm import get_llm

ROUTER_PROMPT = """You route questions to the right document collection.

Collections:
{descriptions}

Reply with ONE of these words only:
{options}

- Use "both" if the question needs both collections.
- Use "none" if the question is not about healthcare licensing or KP health policy.

Question: {question}
Answer:"""


def router_node(state):
    descriptions = "\n".join(f"- {name}: {text}" for name, text in COLLECTIONS.items())
    options = ", ".join(list(COLLECTIONS) + ["both", "none"])

    prompt = ROUTER_PROMPT.format(
        descriptions=descriptions, options=options, question=state["question"]
    )
    reply = get_llm().invoke(prompt).content.strip().lower()

    if "none" in reply:
        chosen = []                                   
    else:
        chosen = [name for name in COLLECTIONS if name in reply]
        if not chosen:                               
            chosen = list(COLLECTIONS)                

    print(f"[router] reply='{reply}' -> collections={chosen}")
    return {"collections": chosen}
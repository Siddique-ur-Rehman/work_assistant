
import json
import uuid

from app.rag.llm import ask_llm

MAX_MEMORIES = 20

EXTRACT_PROMPT = """From this conversation turn, extract lasting facts about the USER
that would help in future chats: their role, organization or district,
topics they work on, and how they like answers written (language, length, format).

Rules:
- Do NOT save policy or legal facts from the answer.
- Do NOT save names, phone numbers, ID numbers, or health details of any person.
- Do NOT repeat anything already in the existing memories.
- Return a JSON list of short strings. Return [] if there is nothing worth saving.

Existing memories:
{existing}

User said: {question}
Assistant replied: {answer}

JSON list:"""


def _namespace(user_id):
    return ("memories", user_id)


def load_memories(store, user_id):
    """Return this user's saved memories as a list of {'key', 'text'}."""
    items = store.search(_namespace(user_id), limit=MAX_MEMORIES)
    return [{"key": item.key, "text": item.value["text"]} for item in items]


def save_new_memories(store, user_id, question, answer):
    """Extract new facts from one turn and save them. Never raises."""
    try:
        existing = load_memories(store, user_id)
        if len(existing) >= MAX_MEMORIES:
            return

        known = {m["text"].lower() for m in existing}
        prompt = EXTRACT_PROMPT.format(
            existing="\n".join(f"- {m['text']}" for m in existing) or "(none)",
            question=question,
            answer=answer[:500],
        )
        reply = ask_llm(prompt, "[]").replace("```json", "").replace("```", "").strip()
        facts = json.loads(reply)

        for fact in facts:
            if isinstance(fact, str) and fact.strip() and fact.lower() not in known:
                store.put(_namespace(user_id), str(uuid.uuid4()), {"text": fact.strip()})
                print(f"[memory] saved: {fact.strip()}")
    except Exception as error:
        print(f"[memory] save skipped: {type(error).__name__}: {error}")


def delete_memory(store, user_id, key):
    store.delete(_namespace(user_id), key)


def delete_all_memories(store, user_id):
    for item in store.search(_namespace(user_id), limit=MAX_MEMORIES):
        store.delete(_namespace(user_id), item.key)
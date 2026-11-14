# Node: load this user's long-term memories at the start of a turn.
from app.memory.memory import load_memories


def load_memory_node(state, config, *, store=None):
    user_id = config["configurable"].get("user_id")
    if store is None or not user_id:
        return {"memories": []}

    memories = [m["text"] for m in load_memories(store, user_id)]
    print(f"[memory] loaded {len(memories)} memories")
    return {"memories": memories}
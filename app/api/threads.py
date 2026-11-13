
from fastapi import APIRouter, Header, HTTPException, Request
from langgraph.errors import GraphRecursionError

from app.api.schemas import ChatIn, RenameIn
from app.rag.llm import ask_llm
from app.sessions import store

router = APIRouter(prefix="/api/v1")


def require_user(x_user_id):
    if not x_user_id:
        raise HTTPException(status_code=400, detail="Missing X-User-Id header")
    return x_user_id


def require_thread(thread_id, user_id):
    """404 if the thread doesn't exist OR belongs to another user."""
    thread = store.get_thread(thread_id, user_id)
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread


@router.post("/threads")
def create_thread(x_user_id: str = Header(None)):
    user_id = require_user(x_user_id)
    return {"thread_id": store.create_thread(user_id)}


@router.get("/threads")
def list_threads(x_user_id: str = Header(None)):
    user_id = require_user(x_user_id)
    return store.list_threads(user_id)


@router.patch("/threads/{thread_id}")
def rename_thread(thread_id: str, body: RenameIn, x_user_id: str = Header(None)):
    user_id = require_user(x_user_id)
    require_thread(thread_id, user_id)
    store.rename_thread(thread_id, user_id, body.title)
    return {"thread_id": thread_id, "title": body.title}


@router.delete("/threads/{thread_id}")
def delete_thread(thread_id: str, request: Request, x_user_id: str = Header(None)):
    user_id = require_user(x_user_id)
    require_thread(thread_id, user_id)
    request.app.state.checkpointer.delete_thread(thread_id)   # removes the messages
    store.delete_thread_row(thread_id, user_id)               # removes the list entry
    return {"deleted": thread_id}


@router.get("/threads/{thread_id}/messages")
def get_messages(thread_id: str, request: Request, x_user_id: str = Header(None)):
    user_id = require_user(x_user_id)
    require_thread(thread_id, user_id)
    config = {"configurable": {"thread_id": thread_id}}
    state = request.app.state.graph.get_state(config)
    messages = state.values.get("messages", [])
    return [{"role": m.type, "content": m.content} for m in messages]


@router.post("/threads/{thread_id}/chat")
def chat(thread_id: str, body: ChatIn, request: Request, x_user_id: str = Header(None)):
    user_id = require_user(x_user_id)
    thread = require_thread(thread_id, user_id)

    config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 25}
    try:
        result = request.app.state.graph.invoke({"question": body.question}, config)
    except GraphRecursionError:
        raise HTTPException(status_code=500, detail="The run hit the step limit")

    
    if thread["title"] == "New chat":
        title = ask_llm(
            f"Write a title of at most 5 words for a chat that starts with: {body.question}\n"
            "Return only the title.",
            body.question[:40],
        ).strip('"')[:100]
        store.rename_thread(thread_id, user_id, title)

    store.touch_thread(thread_id)

    sources = [
        {"collection": d["collection"], "file": d["source"], "page": d["page"]}
        for d in result.get("documents", [])
    ]
    return {"answer": result["answer"], "sources": sources}
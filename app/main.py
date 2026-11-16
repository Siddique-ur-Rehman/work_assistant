
from contextlib import asynccontextmanager
from langgraph.store.postgres import PostgresStore
from pathlib import Path

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI
from langgraph.checkpoint.postgres import PostgresSaver

from app.api.threads import router
from app.graph.nodes.builder import build_graph
from app.sessions.db import pool



@asynccontextmanager
async def lifespan(app):
    pool.open()
    checkpointer = PostgresSaver(pool)
    store=PostgresStore(pool)
    app.state.checkpointer = checkpointer
    app.state.store=store
    app.state.graph = build_graph(checkpointer)
    yield                     
    pool.close()


app = FastAPI(title="Healthcare Policy Assistant", lifespan=lifespan)
app.include_router(router)

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/health")
def health():
    return {"status": "ok"}
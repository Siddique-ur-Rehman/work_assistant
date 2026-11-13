
from contextlib import asynccontextmanager

from fastapi import FastAPI
from langgraph.checkpoint.postgres import PostgresSaver

from app.api.threads import router
from app.graph.nodes.builder import build_graph
from app.sessions.db import pool


@asynccontextmanager
async def lifespan(app):
    pool.open()
    checkpointer = PostgresSaver(pool)
    app.state.checkpointer = checkpointer
    app.state.graph = build_graph(checkpointer)
    yield                     
    pool.close()


app = FastAPI(title="Healthcare Policy Assistant", lifespan=lifespan)
app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}
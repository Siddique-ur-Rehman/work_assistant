from langgraph.graph import StateGraph, START, END

from app.graph.state import GraphState
from app.graph.edges import route_after_router, route_after_grade
from app.graph.nodes.rewrite import rewrite_node
from app.graph.nodes.router import router_node
from app.graph.nodes.retrieve import retrieve_node
from app.graph.nodes.grade import grade_node
from app.graph.nodes.retry_query import retry_query_node
from app.graph.nodes.answer import answer_node
from app.graph.nodes.no_answer import no_answer_node
from app.graph.nodes.chat_history import chat_history_node
from app.graph.nodes.out_of_scope import out_of_scope_node


def build_graph(checkpointer=None):
    graph = StateGraph(GraphState)

    graph.add_node("rewrite", rewrite_node)
    graph.add_node("router", router_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("grade", grade_node)
    graph.add_node("retry_query", retry_query_node)
    graph.add_node("answer", answer_node)
    graph.add_node("no_answer", no_answer_node)
    graph.add_node("chat_history", chat_history_node)
    graph.add_node("out_of_scope", out_of_scope_node)

    graph.add_edge(START, "rewrite")
    graph.add_edge("rewrite", "router")

    graph.add_conditional_edges(
        "router",
        route_after_router,
        {
            "retrieve": "retrieve",
            "chat_history": "chat_history",
            "out_of_scope": "out_of_scope",
        },
    )

    graph.add_edge("retrieve", "grade")

    graph.add_conditional_edges(
        "grade",
        route_after_grade,
        {"answer": "answer", "retry_query": "retry_query", "no_answer": "no_answer"},
    )

    graph.add_edge("retry_query", "retrieve")      

    graph.add_edge("answer", END)
    graph.add_edge("no_answer", END)
    graph.add_edge("chat_history", END)
    graph.add_edge("out_of_scope", END)

    return graph.compile(checkpointer=checkpointer)
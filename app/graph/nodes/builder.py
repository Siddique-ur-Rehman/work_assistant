
from langgraph.graph import StateGraph, START, END

from app.graph.state import GraphState
from app.graph.edges import route_after_router
from app.graph.nodes.router import router_node
from app.graph.nodes.retrieve import retrieve_node
from app.graph.nodes.answer import answer_node
from app.graph.nodes.out_of_scope import out_of_scope_node


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("router", router_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("answer", answer_node)
    graph.add_node("out_of_scope", out_of_scope_node)

    graph.add_edge(START, "router")

    
    graph.add_conditional_edges(
        "router",
        route_after_router,
        {"retrieve": "retrieve", "out_of_scope": "out_of_scope"},
    )

    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", END)
    graph.add_edge("out_of_scope", END)

    return graph.compile()
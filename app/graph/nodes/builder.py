
from langgraph.graph import StateGraph, START, END

from app.graph.state import GraphState
from app.graph.nodes.retrieve import retrieve_node
from app.graph.nodes.answer import answer_node


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("retrieve", retrieve_node)
    graph.add_node("answer", answer_node)

    graph.add_edge(START, "retrieve")
    graph.add_edge("retrieve", "answer")
    graph.add_edge("answer", END)

    return graph.compile()
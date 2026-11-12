
def no_answer_node(state):
    answer = "I don't know based on the available documents."
    return {
        "documents": [],
        "answer": answer,
        "messages": [("user", state["question"]), ("assistant", answer)],
    }
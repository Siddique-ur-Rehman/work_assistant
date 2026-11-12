def out_of_scope_node(state):
    answer = (
        "I can only answer questions about healthcare licensing regulations "
        "and KP health policy. Could you rephrase your question on those topics?"
    )
    return {
        "documents": [],
        "answer": answer,
        "messages": [("user", state["question"]), ("assistant", answer)],
    }
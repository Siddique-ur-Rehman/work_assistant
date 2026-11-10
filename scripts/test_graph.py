
from app.graph.nodes.builder import build_graph

app = build_graph()

result = app.invoke({"question": "How is the Prime Minister of America?"})

print("ANSWER:\n", result["answer"])
print("\nSOURCES:")
for d in result["documents"]:
    print(f"- {d['collection']} | {d['source']} | page {d['page']} | score {d['score']:.3f}")
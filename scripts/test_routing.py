
from app.graph.nodes.builder import build_graph

app = build_graph()


TESTS = [
    ("How will the cancellation of licence occurs according to rules?", ["licensing_regulations"]),
    ("How the health department will develop the training curriculm in collabration with other?", ["health_policy_kpk"]),
    ("What was the vision of kpk health department and also the routine of inspection team in licenceing regulations ?", ["licensing_regulations", "health_policy_kpk"]),
    ("What is the best pizza in Peshawar?", []),
]

correct = 0
for question, expected in TESTS:
    result = app.invoke({"question": question})
    chosen = result["collections"]
    ok = sorted(chosen) == sorted(expected)
    correct += ok
    print(f"\nQ: {question}\n   expected={expected} got={chosen} -> {'OK' if ok else 'WRONG'}")
    print("   answer:", result["answer"][:150])

print(f"\nRouting accuracy: {correct}/{len(TESTS)}")
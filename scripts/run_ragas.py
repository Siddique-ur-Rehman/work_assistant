# Goal: score the whole RAG system with RAGAS.
import asyncio
import json
from pathlib import Path
import re

import pandas as pd

from app.rag.llm import ask_llm

import pandas as pd

from ragas.llms import llm_factory


from app.config.settings import settings
from app.graph.nodes.builder import build_graph

questions = json.loads(Path("tests/eval/questions.json").read_text(encoding="utf-8"))
app = build_graph()


def to_text(reference):
    """Turn a reference (string, dict, or list of dicts) into one plain string."""
    if isinstance(reference, str):
        return reference
    if isinstance(reference, dict):
        reference = [reference]
    parts = []
    for item in reference:
        if isinstance(item, str):
            parts.append(item)
        else:
            parts.extend(
                v for k, v in item.items()
                if isinstance(v, str) and k not in ("source", "file", "page")
            )
    return " ".join(parts)



samples = []
for q in questions:
    if not q["answerable"]:
        continue
    result = app.invoke(
        {"question": q["question"]},
        {"configurable": {"user_id": "eval"}, "recursion_limit": 25},
    )
    samples.append({
        "user_input": q["question"],
        "response": result.get("answer", ""),
        "retrieved_contexts": [d["text"] for d in result.get("documents", [])],
        "reference": to_text(q["reference"]),
    })





def judge(prompt):
    """Ask the LLM for a score from 0 to 10. Returns a number from 0 to 1, or None."""
    reply = ask_llm(prompt + "\nReply with ONLY a number from 0 to 10.", "")
    match = re.search(r"\d+(\.\d+)?", reply)
    return min(float(match.group()), 10) / 10 if match else None


rows = []
for s in samples:
    print("Scoring:", s["user_input"][:60])
    context = "\n\n".join(s["retrieved_contexts"])[:6000]

    rows.append({
        "question": s["user_input"],
        # Is every claim in the answer supported by the context? (hallucination check)
        "faithfulness": judge(
            f"Context:\n{context}\n\nAnswer:\n{s['response']}\n\n"
            "How well is every claim in the answer supported by the context? "
            "10 = fully supported, 0 = not supported."),
        # Does the answer address the question?
        "answer_relevancy": judge(
            f"Question: {s['user_input']}\n\nAnswer:\n{s['response']}\n\n"
            "How directly does the answer address the question? 10 = fully, 0 = not at all."),
        # Are the retrieved chunks relevant to the question? (precision)
        "context_precision": judge(
            f"Question: {s['user_input']}\n\nRetrieved chunks:\n{context}\n\n"
            "What share of these chunks is relevant to the question? 10 = all, 0 = none."),
        # Does the context contain what the reference answer needs? (recall)
        "context_recall": judge(
            f"Reference answer: {s['reference']}\n\nRetrieved chunks:\n{context}\n\n"
            "How much of the reference answer is covered by the chunks? 10 = all, 0 = none."),
    })

df = pd.DataFrame(rows)
print(df)
print("\nAVERAGES")
print(df.drop(columns="question").mean(numeric_only=True))
df.to_csv("docs/ragas_results.csv", index=False)
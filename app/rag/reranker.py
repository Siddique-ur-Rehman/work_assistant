
from sentence_transformers import CrossEncoder


RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

_model = None


def _get_model():
    global _model
    if _model is None:              
        _model = CrossEncoder(RERANK_MODEL)
    return _model


def rerank(question, chunks, top_n=5):
    """Return the top_n chunks, best first. `chunks` are dicts with a 'text' key."""
    if not chunks:
        return []
    pairs = [(question, chunk["text"]) for chunk in chunks]
    scores = _get_model().predict(pairs)
    for chunk, score in zip(chunks, scores):
        chunk["score"] = float(score)     
    chunks.sort(key=lambda c: c["score"], reverse=True)
    return chunks[:top_n]
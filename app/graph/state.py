
from typing import TypedDict


class GraphState(TypedDict, total=False):
    question: str     
    documents: list    
    answer: str        
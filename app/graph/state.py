
from typing import TypedDict,Annotated
from langgraph.graph.message import add_messages
class GraphState(TypedDict, total=False):
    question: str     
    standalone_question:str
    intent:str
    search_query:str
    memories: list 
    retry_count:int
    grade:str
    documents: list   
    collections:list 
    answer: str      
    messages:Annotated[list,add_messages]  
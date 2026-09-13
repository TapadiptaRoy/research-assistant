# Defines the shared state schema passed between LangGraph nodes

from typing import TypedDict, List
from langchain_core.documents import Document

class ResearchState(TypedDict):
    query: str
    sources_to_use: List[str]
    documents: List[Document]
    answer: str
    retries: int
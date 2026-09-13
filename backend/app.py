# FastAPI backend: exposes the LangGraph research pipeline over HTTP

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict
import os

from graph.workflow import build_graph

app = FastAPI(title="Multi-Source Research Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()


class ChatRequest(BaseModel):
    query: str
    history: List[Dict[str, str]] = []


class ChatResponse(BaseModel):
    answer: str
    history: List[Dict[str, str]]
    sources_used: List[str]
    document_sources: List[Dict[str, str]]


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    result = graph.invoke({"query": req.query, "history": req.history})

    document_sources = [
        {
            "title": doc.metadata.get("title", ""),
            "url": doc.metadata.get("url", ""),
            "source": doc.metadata.get("source", ""),
        }
        for doc in result.get("documents", [])
        if doc.page_content.strip()
    ]

    return ChatResponse(
        answer=result["answer"],
        history=result["history"],
        sources_used=result.get("sources_to_use", []),
        document_sources=document_sources,
    )


# Serve the frontend
web_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "interface", "web")
app.mount("/", StaticFiles(directory=web_dir, html=True), name="web")
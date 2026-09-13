# Defines the LangGraph graph: nodes, edges, and control flow
from langgraph.graph import StateGraph, START, END

from router.query_router import route_query
from sources.arxiv_source import search_arxiv
from sources.pubmed_source import search_pubmed
from sources.openalex_source import search_openalex
from sources.web_source import search_web
from synthesis.synthesizer import synthesize
from graph.state import ResearchState


def route_node(state: ResearchState) -> dict:
    return {"sources_to_use": route_query(state["query"])}


def retrieve_node(state: ResearchState) -> dict:
    is_retry = state.get("retries", 0) >= 1

    if is_retry:
        sources = ["arxiv", "pubmed", "openalex", "web"]
        max_results = 5
    else:
        sources = state["sources_to_use"]
        max_results = 3

    print(f"[retrieve_node] Fetching from: {sources} (retry={is_retry})")

    all_docs = []
    if "arxiv" in sources:
        print("[retrieve_node] Calling arxiv...")
        all_docs += search_arxiv(state["query"], max_results=max_results)
    if "pubmed" in sources:
        print("[retrieve_node] Calling pubmed...")
        all_docs += search_pubmed(state["query"], max_results=max_results)
    if "openalex" in sources:
        print("[retrieve_node] Calling openalex...")
        all_docs += search_openalex(state["query"], max_results=max_results)
    if "web" in sources:
        print("[retrieve_node] Calling web...")
        all_docs += search_web(state["query"], max_results=max_results)

    print(f"[retrieve_node] Got {len(all_docs)} docs total")

    return {
        "documents": all_docs,
        "retries": state.get("retries", 0) + 1
    }


def check_documents(state: ResearchState) -> str:
    non_empty_docs = [d for d in state["documents"] if d.page_content.strip()]
    if len(non_empty_docs) >= 2:
        return "enough"
    if state.get("retries", 0) >= 1:
        return "enough"
    return "not_enough"


def synthesize_node(state: ResearchState) -> dict:
    answer = synthesize(state["query"], state["documents"])
    return {"answer": answer}


def build_graph():
    builder = StateGraph(ResearchState)

    builder.add_node("route", route_node)
    builder.add_node("retrieve", retrieve_node)
    builder.add_node("synthesize", synthesize_node)

    builder.add_edge(START, "route")
    builder.add_edge("route", "retrieve")
    builder.add_conditional_edges(
        "retrieve",
        check_documents,
        {
            "enough": "synthesize",
            "not_enough": "retrieve"
        }
    )
    builder.add_edge("synthesize", END)

    return builder.compile()


if __name__ == "__main__":
    graph = build_graph()
    result = graph.invoke({"query": "What is quantum computing?"})
    print(f"Retries used: {result['retries']}")
    print(result["answer"])
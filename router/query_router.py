from langchain_anthropic import ChatAnthropic
from config import ANTHROPIC_API_KEY

def _format_history(history):
    if not history:
        return "No prior conversation."
    parts = []
    for turn in history:
        parts.append(f"Q: {turn['question']}\nA: {turn['answer']}")
    return "\n\n".join(parts)

def route_query(query: str, history=None):
    if history is None:
        history = []

    llm = ChatAnthropic(model="claude-sonnet-4-6", api_key=ANTHROPIC_API_KEY)

    history_block = _format_history(history)

    prompt = f"""Given the conversation so far and a new question, decide which sources are relevant to answer it well.
Available sources: arxiv, pubmed, openalex, web

Conversation so far:
{history_block}

New question: {query}

Respond with ONLY a comma-separated list of relevant source names, nothing else."""

    response = llm.invoke(prompt)
    sources = [s.strip().lower() for s in response.content.split(",")]
    return sources

if __name__ == "__main__":
    print(route_query("What's the latest news on quantum computing breakthroughs?"))
    print(route_query("Explain the mechanism of CRISPR gene editing"))
# Merges results from multiple sources into one synthesized, cited answer
from langchain_anthropic import ChatAnthropic
from config import ANTHROPIC_API_KEY

from sources.arxiv_source import search_arxiv


def build_context(docs):
    parts = []
    for doc in docs:
        text = f"""
Source: {doc.metadata["source"]}
Title: {doc.metadata["title"]}
Content: {doc.page_content}
"""
        parts.append(text)
    return "\n\n".join(parts)


def _format_history(history):
    if not history:
        return "No prior conversation."
    parts = []
    for turn in history:
        parts.append(f"Q: {turn['question']}\nA: {turn['answer']}")
    return "\n\n".join(parts)


def synthesize(query: str, docs, history=None):
    if history is None:
        history = []

    context = build_context(docs)
    history_block = _format_history(history)

    prompt = f"""You are a research assistant having an ongoing conversation with the user.
Use the conversation history to understand follow-up questions and maintain continuity.
Answer the new question using ONLY the sources below. Cite the source name (e.g. "according to arxiv...") for each claim you make.

Conversation so far:
{history_block}

New question: {query}

Sources:
{context}

Answer:"""

    llm = ChatAnthropic(model="claude-sonnet-4-6", api_key=ANTHROPIC_API_KEY)
    response = llm.invoke(prompt)
    return response.content


if __name__ == "__main__":
    query = "What is quantum computing?"
    docs = search_arxiv(query)
    answer = synthesize(query, docs)
    print(answer)
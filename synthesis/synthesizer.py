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

def synthesize(query: str, docs):
    context = build_context(docs)
    
    prompt = f"""You are a research assistant. Answer the user's question using ONLY the sources below.
Cite the source name (e.g. "according to arxiv...") for each claim you make.

Question: {query}

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
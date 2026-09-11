# Decides which source(s) to query based on the user's question
from langchain_anthropic import ChatAnthropic
from config import ANTHROPIC_API_KEY

def route_query(query: str):
    llm = ChatAnthropic(model="claude-sonnet-4-6", api_key=ANTHROPIC_API_KEY)
    
    prompt = f"""Given this question, which sources are relevant to answer it well?
Available sources: arxiv, pubmed, openalex, web

Question: {query}

Respond with ONLY a comma-separated list of relevant source names, nothing else."""

    response = llm.invoke(prompt)
    sources = [s.strip().lower() for s in response.content.split(",")]
    return sources

if __name__ == "__main__":
    print(route_query("What's the latest news on quantum computing breakthroughs?"))
    print(route_query("Explain the mechanism of CRISPR gene editing"))
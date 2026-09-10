from langchain_core.documents import Document
import arxiv

def search_arxiv(query: str, max_results: int = 3):
    client = arxiv.Client()
    search = arxiv.Search(query=query, max_results=max_results)
    results = client.results(search)

    documents = []
    for r in results:
        doc = Document(
            page_content=r.summary,
            metadata={
                "title": r.title,
                "authors": [a.name for a in r.authors],
                "published": str(r.published),
                "url": r.entry_id,
                "source": "arxiv"
            }
        )
        documents.append(doc)

    return documents

if __name__ == "__main__":
    docs = search_arxiv("quantum computing")
    for d in docs:
        print(d.metadata["title"])
        print(d.page_content[:200])
        print("---")
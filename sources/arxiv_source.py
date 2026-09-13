from langchain_core.documents import Document
import arxiv
def search_arxiv(query: str, max_results: int = 3):
    client = arxiv.Client()
    search = arxiv.Search(query=query, max_results=max_results)

    documents = []
    try:
        results = client.results(search)
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
    except Exception as e:
        print(f"arXiv search failed: {e}")

    return documents
from langchain_community.retrievers import PubMedRetriever
from langchain_core.documents import Document

def search_pubmed(query: str, max_results: int = 3):
    retriever = PubMedRetriever()
    docs = retriever.invoke(query)

    documents = []
    for d in docs[:max_results]:
        doc = Document(
            page_content=d.page_content,
            metadata={
                "title": d.metadata.get("Title", ""),
                "authors": [],
                "published": d.metadata.get("Published", ""),
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{d.metadata.get('uid', '')}/",
                "source": "pubmed"
            }
        )
        documents.append(doc)

    return documents

if __name__ == "__main__":
    results = search_pubmed("quantum computing")
    for d in results:
        print(d.metadata["title"])
        print(d.page_content[:200])
        print("---")
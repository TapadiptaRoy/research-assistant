from langchain_community.retrievers import PubMedRetriever
from langchain_core.documents import Document


def _stringify(value):
    """PubMed's XML sometimes nests tags (e.g. <i>italic</i> in a title),
    which xmltodict turns into a dict like {'i': '...', '#text': '...'}
    instead of a plain string. This flattens any such value into plain text."""
    if isinstance(value, dict):
        return _stringify(value.get("#text", ""))
    if isinstance(value, list):
        return " ".join(_stringify(v) for v in value)
    if value is None:
        return ""
    return str(value)


def search_pubmed(query: str, max_results: int = 3):
    documents = []
    try:
        retriever = PubMedRetriever()
        docs = retriever.invoke(query)

        for d in docs[:max_results]:
            doc = Document(
                page_content=_stringify(d.page_content),
                metadata={
                    "title": _stringify(d.metadata.get("Title", "")),
                    "authors": [],
                    "published": _stringify(d.metadata.get("Published", "")),
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{d.metadata.get('uid', '')}/",
                    "source": "pubmed"
                }
            )
            documents.append(doc)
    except Exception as e:
        print(f"PubMed search failed: {e}")

    return documents


if __name__ == "__main__":
    results = search_pubmed("quantum computing")
    for d in results:
        print(d.metadata["title"])
        print(d.page_content[:200])
        print("---")
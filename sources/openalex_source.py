import requests
from langchain_core.documents import Document

def _rebuild_abstract(inverted_index):
    if not inverted_index:
        return ""
    max_pos = max(pos for positions in inverted_index.values() for pos in positions)
    words = [""] * (max_pos + 1)
    for word, positions in inverted_index.items():
        for pos in positions:
            words[pos] = word
    return " ".join(words)

def search_openalex(query: str, max_results: int = 3):
    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "per_page": max_results
    }
    response = requests.get(url, params=params)
    data = response.json()

    documents = []
    for paper in data.get("results", []):
        abstract = _rebuild_abstract(paper.get("abstract_inverted_index"))
        authors = [a["author"]["display_name"] for a in paper.get("authorships", [])]

        doc = Document(
            page_content=abstract,
            metadata={
                "title": paper.get("title", ""),
                "authors": authors,
                "published": paper.get("publication_year", ""),
                "url": paper.get("id", ""),
                "source": "openalex"
            }
        )
        documents.append(doc)

    return documents

if __name__ == "__main__":
    results = search_openalex("quantum computing")
    for d in results:
        print(d.metadata["title"])
        print(d.metadata["authors"])
        print(d.page_content[:200])
        print("---")
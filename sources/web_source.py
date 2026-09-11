from langchain_tavily import TavilySearch
from langchain_core.documents import Document
from config import TAVILY_API_KEY

def search_web(query: str, max_results: int = 3):
    tool = TavilySearch(max_results=max_results, tavily_api_key=TAVILY_API_KEY)
    response = tool.invoke(query)

    documents = []
    for item in response["results"]:
        doc = Document(
            page_content=item.get("content", "").strip(),
            metadata={
                "title": item.get("title", "").strip(),
                "url": item.get("url", "").strip(),
                "authors": [],
                "published": item.get("published_date", ""),
                "source": "web",

            }
        )
        documents.append(doc)

    return documents

if __name__ == "__main__":
    results = search_web("latest news on quantum computing")
    for d in results:
        print(d.metadata["title"])
        print(d.page_content[:200])
        print("---")
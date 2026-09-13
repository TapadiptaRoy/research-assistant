# Command-line entry point for interacting with the assistant
# Command-line entry point for interacting with the assistant

from graph.workflow import build_graph

def main():
    graph = build_graph()
    print("Multi-Source Research Assistant")
    print("Type your question, or 'quit' to exit.\n")

    while True:
        query = input("You: ").strip()

        if query.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        if not query:
            continue

        result = graph.invoke({"query": query})
        print("\nAssistant:\n")
        print(result["answer"])
        print("\n" + "-" * 60 + "\n")

if __name__ == "__main__":
    main()
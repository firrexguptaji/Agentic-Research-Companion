import sys
from graph.research_graph import build_graph


def main():
    if len(sys.argv) < 2:
        print("Usage: python run.py \"<query>\" [pdf_path]")
        sys.exit(1)

    query = sys.argv[1]

    # IMPORTANT: this must be index 2
    paper_path = sys.argv[2] if len(sys.argv) > 2 else None

    print("DEBUG paper_path:", paper_path)

    state = {
        "query": query,
        "paper_path": paper_path,
        "paper_text": "",
        "selected_agents": [],
        "intermediate_results": {},
        "final_response": "",
    }

    graph = build_graph()
    result = graph.invoke(state)

    print("\n================ FINAL RESPONSE ================\n")
    print(result["final_response"])
    print("\n================================================\n")


if __name__ == "__main__":
    main()
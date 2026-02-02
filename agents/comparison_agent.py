from typing import Dict, List
from tools.vector_store import PaperVectorStore

def comparison_agent(state: dict) -> dict:
    # """
    # Comparison Agent (Stage 1)
    # -------------------------
    # Stimulates comparison between this paper and other
    # related works (e.g., baseline models).
    
    # Stage 1 behavior:
    # - No multi-paper retrieval
    # - No vector search
    # - No metrics parsing
    
    # Input:
    #     state: shared LangGraph state
    
    # Output:
    #     Updated state with comparison placeholder
    # """

    """
    Comparison Agent (Stage 3.2)
    ----------------------------
    Uses VectorDB to retrieve semantically relevant sections
    related to methods, results, and performance, and produces
    a grounded comparison-style summary.
    """

    query = state.get("query", "")
    paper_text = state.get("paper_text", "")

    vector_store = PaperVectorStore()

    # 🔍 Semantic retrieval focused on comparison-relevant content
    retrieved_chunks: List[Dict] = vector_store.query(
        query="method approach results performance comparison baseline",
        top_k=3,
    )

    if not paper_text.strip():
        explanation = (
            "No paper text available. Unable to perform a comparison."
        )
        evidence = []

    elif retrieved_chunks:
        explanation = (
            "Based on semantically relevant sections retrieved from the paper, "
            "the comparison focuses on differences in methodology, experimental "
            "setup, and reported performance. Key comparative contexts are shown below."
        )
        evidence = retrieved_chunks

    else:
        explanation = (
            "No strongly comparison-relevant sections were retrieved from the paper. "
            "The paper may not explicitly compare against baselines in the extracted text, "
            "or such comparisons may be presented in figures or tables."
        )
        evidence = []

    state["intermediate_results"]["comparison"] = {
        "query": query,
        "explanation": explanation,
        "retrieved_contexts": evidence,
    }

    return state
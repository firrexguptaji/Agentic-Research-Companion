from typing import Dict, List
from tools.vector_store import PaperVectorStore


def math_explainer_agent(state: dict) -> dict:
    """
    Math Explainer Agent (Stage 3.1)
    --------------------------------
    Uses VectorDB to retrieve semantically relevant
    content related to loss/objective functions.
    """
    query = state.get("query", "")
    vector_store = state.get("vector_store")

    if not vector_store:
        explanation = "No vector store available."
        contexts = []
    else:
        contexts = vector_store.similarity_search(
            query,
            top_k=3,
            section_filter="method",
        )

        if not contexts:
            explanation = (
                "The paper does not explicitly define a loss function. "
                "The objective appears implicit or described outside text."
            )
        else:
            explanation = (
                "Based on the retrieved mathematical context, "
                "the loss function optimizes model predictions against targets."
            )

    state["intermediate_results"]["math_explainer"] = {
        "query": query,
        "explanation": explanation,
        "retrieved_contexts": contexts,
    }

    return state
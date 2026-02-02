from tools import vector_store


LOSS_SECTION_PRIORITY = [
    "training",
    "training details",
    "optimization",
    "model",
    "architecture",
    "method",
    "experiments",
    "full_text",
]

def math_explainer_agent(state: dict) -> dict:
    query = state.get("query", "")
    vector_store = state.get("vector_store")

    if not vector_store:
        explanation = (
            "No paper was provided, so this is a general explanation.\n\n"
            "A loss function measures how far a model’s predictions are from the "
            "correct targets. During training, the model updates its parameters "
            "to minimize this loss. Common examples include mean squared error "
            "for regression tasks and cross-entropy loss for classification or "
            "sequence modeling."
        )
        contexts = []
    else:
        contexts = []
        for section in LOSS_SECTION_PRIORITY:
            section_contexts = vector_store.similarity_search(
                query,
                top_k=3,
                section_filter=section,
            )
            if section_contexts:
                contexts.extend(section_contexts)
                break
        if contexts:
            explanation = (
                "Based on the paper, the loss function is used to optimize model "
                "predictions against ground-truth targets. The retrieved sections "
                "describe how this objective guides training."
            )
        else:
            explanation = (
                "The paper does not explicitly define a loss function in the main text. "
                "The optimization objective may be implicit or described elsewhere."
            )

    state["intermediate_results"]["math_explainer"] = {
        "query": query,
        "explanation": explanation,
        "retrieved_contexts": contexts,
    }

    return state
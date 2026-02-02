import re
from typing import Dict, List
from tools.vector_store import PaperVectorStore


LOSS_PATTERNS = [
    r"loss function",
    r"objective function",
    r"training loss",
    r"we minimize",
    r"we optimise",
    r"we optimize",
    r"\bloss\b",
    r"\bobjective\b",
    r"\bminimi[sz]e\b",
    r"\boptimi[sz]e\b",
    r"\bL\s*\(",      # L(
    r"\bJ\s*\(",      # J(
]

def extract_math_snippets(text: str, window: int = 400) -> Dict[str, str]:
    """
    Extract small text windows around math/loss keywords.
    """
    snippets = {}
    lower = text.lower()

    for i, pat in enumerate(LOSS_PATTERNS):
        m = re.search(pat, lower)
        if m:
            start = max(0, m.start() - window)
            end = min(len(text), m.end() + window)
            snippets[f"snippet_{i+1}"] = text[start:end]
            # stop early once we have a few useful snippets
            if len(snippets) >= 3:
                break

    return snippets


def math_explainer_agent(state: dict) -> dict:
    # """
    # Math Explainer Agent (Stage 2)
    # -----------------------------
    # Uses real paper text to identify and explain loss functions / equations.
    # """
    """
    Math Explainer Agent (Stage 3.1)
    --------------------------------
    Uses VectorDB to retrieve semantically relevant sections
    related to loss/objective functions and explains them.
    """
    
    paper_text = state.get("paper_text", "")
    query = state.get("query", "")
    
    vector_store = PaperVectorStore()

    retrieved_chunks: List[Dict] = vector_store.query(
        query="loss function objective training optimization",
        top_k=3,
    )
    
    if not paper_text.strip():
        explanation = (
            "No paper text available. "
            "Unable to extract or explain loss functions."
        )
        snippets = {}
    else:
        snippets = extract_math_snippets(paper_text)

        if snippets:
            explanation = (
                "Identified candidate loss/objective descriptions in the paper. "
                "Below are extracted contexts where the loss function is discussed. "
                "A full mathematical breakdown would be applied here in later stages."
            )
        else:
            explanation = (
                "The paper does not explicitly define a loss function in the extracted text. "
                "Based on surrounding training-related context, the optimization objective "
                "likely focuses on reducing prediction error between model outputs and targets. "
                "A precise loss definition may be present in figures or supplementary material."
            )


    state["intermediate_results"]["math_explainer"] = {
        "query": query,
        "explanation": explanation,
        "extracted_contexts": snippets,
    }

    return state
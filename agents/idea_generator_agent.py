def idea_generator_agent(state: dict) -> dict:
    """
    Idea Generator Agent (Stage 1)
    -----------------------------
    Simulates generation of future research ideas
    and possible extensions of the paper.

    Stage 1 behavior:
    - No novelty checking
    - No feasibility validation
    - No literature grounding

    Input:
        state: shared LangGraph state

    Output:
        Updated state with future work placeholder
    """

    query = state.get("query", "")

    ideas = (
        "Idea Generator Agent: "
        "This agent would propose future research directions, "
        "possible extensions, hybrid approaches, or additional "
        "experiments that could improve or expand upon the paper."
    )

    state["intermediate_results"]["idea_generator"] = {
        "query": query,
        "ideas": ideas
    }

    return state
def critique_agent(state: dict) -> dict:
    """
    Critique Agent (Stage 1)
    -----------------------
    Simulates a peer-review style critique of the paper.

    Stage 1 behavior:
    - No experiment validation
    - No dataset inspection
    - No claim verification

    Input:
        state: shared LangGraph state

    Output:
        Updated state with critique placeholder
    """

    query = state.get("query", "")

    critique_summary = (
        "Critique Agent: "
        "This agent would analyze the paper from a reviewer’s "
        "perspective, identifying potential limitations, "
        "assumptions, missing baselines, and areas where "
        "claims may be weak or unsupported."
    )

    state["intermediate_results"]["critique"] = {
        "query": query,
        "critique": critique_summary
    }

    return state
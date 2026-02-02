def comparison_agent(state: dict) -> dict:
    """
    Comparison Agent (Stage 1)
    -------------------------
    Stimulates comparison between this paper and other
    related works (e.g., baseline models).
    
    Stage 1 behavior:
    - No multi-paper retrieval
    - No vector search
    - No metrics parsing
    
    Input:
        state: shared LangGraph state
    
    Output:
        Updated state with comparison placeholder
    """
    
    query = state.get("query","")
    
    comparison_agent = (
        "Comparison Agent: "
        "This agent would compare the current paper with "
        "related works or baseline models, highlighting "
        "key differences in methodology, performance, "
        "and assumptions."
    )
    
    state["intermediate_results"]["comparison"] = {
        "query": query,
        "comparison": comparison_agent
    }
    
    return state
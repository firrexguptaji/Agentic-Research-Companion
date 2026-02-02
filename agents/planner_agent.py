from typing import List

def planner_agent(query: str) -> List[str]:
    """
    Plainner Agent(Stage 1)
    ----------------------
    Decides which agent should be invoked based on the user's query.
    
    
    - No tools
    - No vector DB
    - Deterministic , rule-based routing"""
    
    query_lower = query.lower()
    selected_agents: List[str] = []
    
    
    #Always include paper reader first
    selected_agents.append("paper_reader")
    
    #Math / equation
    math_keyword = {
        "equation", "math",
        "calculate","loss",
        "formula","derivation",
        "objective","proof"
    }
    if any(k in query_lower for k in math_keyword):
        selected_agents.append("math_explainer_agent")
        
    #Comparison
    comparison_keyword = {
        "compare", "comparison",
        "vs", "versus",
        "difference", "better than",
        "worse than", "outperform"
    }
    if any(k in query_lower for k in comparison_keyword):
        selected_agents.append("comparison_agent")
        
        
    #Critique / Review
    critique_keyword = {
        "limitations", "limitations",
        "weakness", "issue",
        "critique", "review",
    }
    
    if any(k in query_lower for k in critique_keyword):
        selected_agents.append("critique_agent")
        
    #Futture work / Ideas
    idea_keyword = {
        "future", "improvement",
        "improve", "extension",
        "next step", "research idea",
    }
    if any(k in query_lower for k in idea_keyword):
        selected_agents.append("idea_generator")
        
    #Remover duplicates while preserving order
    seen = set()
    ordered_agents = []
    for agent in selected_agents:
        if agent not in seen:
            seen.add(agent)
            ordered_agents.append(agent)
    
    return ordered_agents
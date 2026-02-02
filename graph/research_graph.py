from typing import TypedDict, Dict, List

from langgraph.graph import StateGraph, END

from agents.planner_agent import planner_agent
from agents.paper_reader_agent import paper_reader_agent
from agents.math_explainer_agent import math_explainer_agent
from agents.comparison_agent import comparison_agent
from agents.critique_agent import critique_agent
from agents.idea_generator_agent import idea_generator_agent


# -----------------------------
# Shared State Definition
# -----------------------------


class ResearchState(TypedDict):
    query: str
    selected_agents: List[str]
    intermediate_results: Dict
    final_response: str

# ----------------------------
# Planner Node
# ----------------------------
def planner_node(state: ResearchState) -> ResearchState:
    selected = planner_agent(state["query"])
    state["selected_agents"] = selected
    return state


# ----------------------------
# Agent Router
# ----------------------------

def agent_router(state: ResearchState) -> str:
    """
    Decides which agent to call next based on
    remaining selected agents.
    """
    if not state["selected_agents"]:
        return "final"
    
    return state["selected_agents"].pop(0)

# ----------------------------
# Final Aggregator
# ----------------------------

def final_node(state: ResearchState) -> ResearchState:
    summaries = []
    
    for agent, result in state["intermediate_results"].items():
        summaries.append(f"[{agent.upper()}]\n{result}")
    
    state["final_response"] = "\n\n".join(summaries)
    return state

# ----------------------------
# Build Graph
# ----------------------------
def build_graph():
    graph = StateGraph(ResearchState)
    
    # Node
    graph.add_node("plainer",planner_node)
    graph.add_node("paper_reader",paper_reader_agent)
    graph.add_node("math_explainer",math_explainer_agent)
    graph.add_node("comparison",comparison_agent)
    graph.add_node("critique",critique_agent)
    graph.add_node("idea_generator",idea_generator_agent)
    graph.add_node("final",final_node)
    
    
    # Edges
    graph.set_entry_point("planner")
    
    graph.add_conditional_edges(
        "plainer",
        agent_router,
        {
            "paper_reader": "paper_reader",
            "math_explainer": "math_explainer",
            "comparison": "comparison",
            "critique": "critique",
            "idea_generator": "idea_generator",
            "final": "final",
        },
    )
    
    for agent in [
        "paper_reader",
        "math_explainer",
        "comparison",
        "critique",
        "idea_generator",
    ]:
        graph.add_conditional_edges(
            agent,
            agent_router,
            {
                "paper_reader": "paper_reader",
                "math_explainer": "math_explainer",
                "comparison": "comparison",
                "critique": "critique",
                "idea_generator": "idea_generator",
                "final": "final",
            },
        )
    
    graph.add_edge("final",END)
    
    return graph.compile()
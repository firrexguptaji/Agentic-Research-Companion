from typing import TypedDict, Dict, List

from langgraph.graph import StateGraph, END

from agents.planner_agent import planner_agent
from agents.paper_reader_agent import paper_reader_agent
from agents.math_explainer_agent import math_explainer_agent
from agents.comparison_agent import comparison_agent
from agents.critique_agent import critique_agent
from agents.idea_generator_agent import idea_generator_agent


# -----------------------------
# Shared State
# -----------------------------
class ResearchState(TypedDict):
    query: str
    selected_agents: List[str]
    intermediate_results: Dict
    final_response: str


# -----------------------------
# Planner Node
# -----------------------------
def planner_node(state: ResearchState) -> ResearchState:
    state["selected_agents"] = planner_agent(state["query"])
    return state


# -----------------------------
# Router
# -----------------------------
def router(state: ResearchState) -> str:
    if not state["selected_agents"]:
        return "final"

    raw_agent = state["selected_agents"].pop(0)

    if raw_agent not in PLANNER_TO_GRAPH_NODE:
        raise ValueError(
            f"Planner returned unknown agent '{raw_agent}'. "
            f"Known agents: {list(PLANNER_TO_GRAPH_NODE.keys())}"
        )

    return PLANNER_TO_GRAPH_NODE[raw_agent]


# -----------------------------
# Final Aggregator
# -----------------------------
def final_node(state: ResearchState) -> ResearchState:
    output = []

    for agent, content in state["intermediate_results"].items():
        output.append(f"[{agent.upper()}]\n{content}")

    state["final_response"] = "\n\n".join(output)
    return state
# -----------------------------
# Planner → Graph Node Mapping
# -----------------------------
PLANNER_TO_GRAPH_NODE = {
    # direct
    "paper_reader": "paper_reader",
    "idea_generator": "idea_generator",

    # math
    "math_explainer_agent": "math_explainer",
    "math_explainer": "math_explainer",

    # comparison
    "comparison_agent": "comparison",
    "comparison": "comparison",

    # critique
    "critique_agent": "critique",
    "critique": "critique",

    # final
    "final": "final",
}

# -----------------------------
# Build Graph
# -----------------------------
def build_graph():
    graph = StateGraph(ResearchState)

    # Nodes
    graph.add_node("planner", planner_node)
    graph.add_node("paper_reader", paper_reader_agent)
    graph.add_node("math_explainer", math_explainer_agent)
    graph.add_node("comparison", comparison_agent)
    graph.add_node("critique", critique_agent)
    graph.add_node("idea_generator", idea_generator_agent)
    graph.add_node("final", final_node)
    
    

    # Entry
    graph.set_entry_point("planner")

    # Planner routes once
    graph.add_conditional_edges(
        "planner",
        router,
        {
            "paper_reader": "paper_reader",
            "math_explainer": "math_explainer",
            "comparison": "comparison",
            "critique": "critique",
            "idea_generator": "idea_generator",
            "final": "final",
        },
    )

    # Agents route to next agent or final
    for agent in [
        "paper_reader",
        "math_explainer",
        "comparison",
        "critique",
        "idea_generator",
    ]:
        graph.add_conditional_edges(
            agent,
            router,
            {
                "paper_reader": "paper_reader",
                "math_explainer": "math_explainer",
                "comparison": "comparison",
                "critique": "critique",
                "idea_generator": "idea_generator",
                "final": "final",
            },
        )

    graph.add_edge("final", END)

    return graph.compile()
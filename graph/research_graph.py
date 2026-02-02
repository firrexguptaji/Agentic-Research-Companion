from typing import TypedDict, Dict, List, Any

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
class ResearchState(TypedDict, total=False):
    # Core
    query: str
    selected_agents: List[str]
    intermediate_results: Dict
    final_response: str

    # Paper-related
    paper_path: str
    paper_text: str
    paper_sections: Dict

    # Vector DB
    vector_store: Any


# -----------------------------
# Planner Node
# -----------------------------
def planner_node(state: ResearchState) -> ResearchState:
    query = state["query"]
    paper_present = bool(state.get("paper_path"))

    state["selected_agents"] = planner_agent(
        query=query,
        paper_present=paper_present,
    )

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
# Router
# -----------------------------
def router(state: ResearchState) -> str:
    selected = state.get("selected_agents", [])

    if not selected:
        return "final"

    raw_agent = selected.pop(0)

    # Explicit write-back (defensive clarity)
    state["selected_agents"] = selected

    mapped = PLANNER_TO_GRAPH_NODE.get(raw_agent)
    if not mapped:
        raise ValueError(
            f"Planner returned unknown agent '{raw_agent}'. "
            f"Known agents: {sorted(PLANNER_TO_GRAPH_NODE.keys())}"
        )

    return mapped


# -----------------------------
# Final Aggregator
# -----------------------------
def final_node(state: ResearchState) -> ResearchState:
    output = []

    for agent, content in state.get("intermediate_results", {}).items():
        output.append(f"[{agent.upper()}]\n{content}")

    state["final_response"] = "\n\n".join(output)
    return state


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

    # Planner routing
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

    # Agent chaining
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
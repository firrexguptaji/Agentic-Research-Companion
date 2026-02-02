from typing import List


def planner_agent(query: str, paper_present: bool) -> List[str]:
    """
    Stage 4 Planner
    - Decides which agents to invoke
    - Uses paper availability as signal
    """

    query_lower = query.lower()
    plan: List[str] = []

    # Read paper only if provided
    if paper_present:
        plan.append("paper_reader")

    # Math / loss / equations
    if any(k in query_lower for k in [
        "loss", "objective", "equation", "derive", "math"
    ]):
        plan.append("math_explainer")

    # Comparison
    if any(k in query_lower for k in [
        "compare", "vs", "baseline", "difference"
    ]):
        plan.append("comparison")

    # Critique
    if any(k in query_lower for k in [
        "limitation", "weakness", "drawback", "issue"
    ]):
        plan.append("critique")

    # Ideas / future work
    if any(k in query_lower for k in [
        "future", "improve", "extension", "idea"
    ]):
        plan.append("idea_generator")

    return plan
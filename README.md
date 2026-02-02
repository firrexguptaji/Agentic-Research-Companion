🧠 Agentic Research Companion — Stage 1

An agent-based research paper analysis system built with LangGraph, demonstrating planner-driven orchestration, modular agents, and production-style routing patterns.

Stage 1 focus: Core agentic architecture & execution flow
No tools, no PDF parsing, no VectorDB — by design.

🚀 What This Project Demonstrates

Multi-agent system design using LangGraph

Planner → Router → Agents → Final aggregation pattern

Deterministic, debuggable agent execution

Clean separation between intent (planner) and execution (graph)

Production-style adapter-based routing (non-brittle)

This stage establishes a scalable foundation for advanced agentic reasoning.

🧩 Implemented Agents

| Agent | Responsibility |
|-------|-----------------|
| Planner Agent | Interprets user intent and selects agents |
| Paper Reader Agent | Simulates understanding paper structure |
| Math Explainer Agent | Simulates explanation of equations & loss |
| Comparison Agent | Simulates comparison with related work |
| Critique Agent | Simulates reviewer-style critique |
| Idea Generator Agent | Simulates future research directions |

Each agent:

Is independently testable

Operates on shared state

Has a single, well-defined responsibility

🔀 Execution Flow (LangGraph)

Example query:

"Compare this paper and explain the loss function"

Execution sequence:

planner
→ paper_reader
→ math_explainer
→ comparison
→ final

The planner runs once

Agents execute sequentially

State is propagated across nodes

The final node aggregates results

🧠 Planner–Router Architecture (Key Design)
Planner

Rule-based

Outputs semantic agent names (intent-focused)

Example output:

["paper_reader", "math_explainer_agent", "comparison_agent"]
Router (Adapter Pattern)

Translates planner intent → graph execution nodes

Prevents hard coupling between planner and graph

Makes the system robust to refactors

This pattern mirrors real-world agent orchestration systems.

🗂️ Project Structure (Stage 1)
agentic-research-companion/
│
├── agents/
│   ├── planner_agent.py
│   ├── paper_reader_agent.py
│   ├── math_explainer_agent.py
│   ├── comparison_agent.py
│   ├── critique_agent.py
│   └── idea_generator_agent.py
│
├── graph/
│   └── research_graph.py
│
├── run.py
├── requirements.txt
└── README.md
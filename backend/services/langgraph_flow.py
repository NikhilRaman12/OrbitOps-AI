from __future__ import annotations

from typing import Any, Dict, List

from backend.agents.cicd_agent import cicd_agent
from backend.agents.code_quality_agent import code_quality_agent
from backend.agents.documentation_agent import documentation_agent
from backend.agents.executive_agent import executive_agent
from backend.agents.ml_governance_agent import ml_governance_agent
from backend.agents.release_agent import release_agent
from backend.agents.repository_agent import repository_agent
from backend.agents.risk_agent import risk_agent
from backend.agents.security_agent import security_agent
from backend.services.mcp_tools import gitlab_orbit_context_tool
from backend.services.state import OrbitState, initial_state

AGENT_SEQUENCE = [
    repository_agent,
    code_quality_agent,
    security_agent,
    ml_governance_agent,
    documentation_agent,
    cicd_agent,
    release_agent,
    risk_agent,
    executive_agent,
]


def build_graph() -> Any:
    """Build a LangGraph StateGraph when langgraph is installed.

    The API falls back to deterministic sequential execution so the hackathon
    demo remains runnable in restricted environments.
    """
    try:
        from langgraph.graph import END, StateGraph
    except Exception:
        return None

    graph = StateGraph(OrbitState)
    names = [
        "repository",
        "code_quality",
        "security",
        "ml_governance",
        "documentation",
        "cicd",
        "release",
        "risk",
        "executive",
    ]
    for name, fn in zip(names, AGENT_SEQUENCE):
        graph.add_node(name, fn)
    graph.set_entry_point("repository")
    for current, next_name in zip(names, names[1:]):
        graph.add_edge(current, next_name)
    graph.add_edge(names[-1], END)
    return graph.compile()


def run_orbitops_graph(
    repository_path: str | None = None,
    repository_url: str | None = None,
    branch: str = "main",
) -> OrbitState:
    context = gitlab_orbit_context_tool(repository_url, branch)
    context["local_path"] = repository_path or "."
    state = initial_state(context)
    graph = build_graph()
    if graph:
        return graph.invoke(state)
    for agent in AGENT_SEQUENCE:
        state = agent(state)
    return state


def agent_timeline(state: OrbitState) -> List[Dict[str, Any]]:
    return [
        {
            "agent": message["sender"],
            "handoff_to": message["receiver"],
            "intent": message["intent"],
            "timestamp": message["timestamp"],
        }
        for message in state.get("a2a_messages", [])
    ]


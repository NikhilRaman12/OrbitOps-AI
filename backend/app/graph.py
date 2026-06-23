from __future__ import annotations
from typing import Any, Dict, List
from backend.app.agents import (
    repository_agent,
    security_agent,
    dependency_agent,
    documentation_agent,
    cicd_agent,
    ml_governance_agent,
    release_decision_agent,
    executive_report_agent,
)
from backend.app.tools.mcp_tools import gitlab_orbit_context_tool
from backend.app.state import OrbitState, initial_state

AGENT_SEQUENCE = [
    repository_agent,
    security_agent,
    dependency_agent,
    documentation_agent,
    cicd_agent,
    ml_governance_agent,
    release_decision_agent,
    executive_report_agent,
]

def build_graph() -> Any:
    """Build a LangGraph StateGraph when langgraph is installed.
    Falls back to sequential execution in restricted environments.
    """
    try:
        from langgraph.graph import END, StateGraph
    except Exception:
        return None

    graph = StateGraph(OrbitState)
    names = [
        "repository",
        "security",
        "dependency",
        "documentation",
        "cicd",
        "ml_governance",
        "release_decision",
        "executive_report",
    ]
    
    # Register nodes
    for name, fn in zip(names, AGENT_SEQUENCE):
        graph.add_node(name, fn)
        
    graph.set_entry_point("repository")
    
    # Add sequential edges
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
    
    compiled_graph = build_graph()
    if compiled_graph:
        try:
            return compiled_graph.invoke(state)
        except Exception:
            # Graceful fallback to sequential list if invocation fails
            pass
            
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

from __future__ import annotations

from typing import Callable

from backend.services.a2a_protocol import mark_agent, send_handoff
from backend.services.state import OrbitState


AgentFn = Callable[[OrbitState], OrbitState]


def run_agent(
    state: OrbitState,
    agent_name: str,
    next_agent: str,
    intent: str,
    fn: AgentFn,
) -> OrbitState:
    mark_agent(state, agent_name, "running")
    state = fn(state)
    mark_agent(state, agent_name, "completed")
    return send_handoff(state, agent_name, next_agent, intent)


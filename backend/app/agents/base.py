from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Callable, Dict
from uuid import uuid4
from backend.app.state import OrbitState

AgentFn = Callable[[OrbitState], OrbitState]

def send_handoff(
    state: OrbitState,
    sender: str,
    receiver: str,
    intent: str,
    payload: Dict[str, Any] | None = None,
) -> OrbitState:
    message = {
        "id": str(uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "sender": sender,
        "receiver": receiver,
        "intent": intent,
        "payload": payload or {},
    }
    state.setdefault("a2a_messages", []).append(message)
    return state

def mark_agent(state: OrbitState, agent: str, status: str) -> OrbitState:
    state.setdefault("agent_status", {})[agent] = status
    return state

def run_agent(
    state: OrbitState,
    agent_name: str,
    next_agent: str,
    intent: str,
    fn: AgentFn,
) -> OrbitState:
    state = mark_agent(state, agent_name, "running")
    state = fn(state)
    state = mark_agent(state, agent_name, "completed")
    state = send_handoff(state, agent_name, next_agent, intent)
    return state

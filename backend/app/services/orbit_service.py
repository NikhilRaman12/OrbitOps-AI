from __future__ import annotations
from pathlib import Path
from typing import Any, Dict
from uuid import uuid4
from backend.app.graph import agent_timeline, run_orbitops_graph

class OrbitOpsService:
    def __init__(self) -> None:
        self._last_state: Dict[str, Any] = {}
        self._runs: Dict[str, Dict[str, Any]] = {}

    def run(self, repository_path: str | None = None, repository_url: str | None = None, branch: str = "main") -> Dict[str, Any]:
        path = str(Path(repository_path or ".").resolve())
        state = run_orbitops_graph(path, repository_url, branch)
        state["timeline"] = agent_timeline(state)
        
        # Add run metadata
        run_id = str(uuid4())
        state["run_id"] = run_id
        
        self._last_state = state
        self._runs[run_id] = state
        return state

    def last_state(self) -> Dict[str, Any]:
        if not self._last_state:
            return self.run(".")
        return self._last_state

    def get_run(self, run_id: str) -> Dict[str, Any] | None:
        return self._runs.get(run_id)

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.services.mcp_tools import documentation_analyzer_tool, release_assessment_tool, security_scanner_tool
from backend.services.orbit_service import OrbitOpsService


class RepositoryRequest(BaseModel):
    repository_path: str | None = Field(default=".", description="Local repository path to analyze")
    repository_url: str | None = Field(default=None, description="GitLab repository URL for Orbit context")
    branch: str = "main"


app = FastAPI(
    title="OrbitOps AI",
    description="Autonomous DevMLSecOps Intelligence Platform powered by GitLab Orbit context.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = OrbitOpsService()


@app.get("/")
def root() -> Dict[str, str]:
    return {"name": "OrbitOps AI", "status": "online", "tagline": "Autonomous DevMLSecOps Intelligence Platform"}


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "healthy"}


@app.get("/dashboard")
def dashboard() -> Dict[str, Any]:
    return service.last_state()


@app.post("/api/analyze/repository")
def analyze_repository(request: RepositoryRequest) -> Dict[str, Any]:
    return service.run(request.repository_path, request.repository_url, request.branch)


@app.post("/api/analyze/security")
def analyze_security(request: RepositoryRequest) -> Dict[str, Any]:
    path = str(Path(request.repository_path or ".").resolve())
    return security_scanner_tool(path)


@app.post("/api/analyze/release")
def analyze_release(request: RepositoryRequest) -> Dict[str, Any]:
    state = service.run(request.repository_path, request.repository_url, request.branch)
    return release_assessment_tool(state)


@app.post("/api/orbitops/run")
def run_orbitops(request: RepositoryRequest) -> Dict[str, Any]:
    return service.run(request.repository_path, request.repository_url, request.branch)


@app.get("/api/a2a/messages")
def a2a_messages() -> Dict[str, Any]:
    state = service.last_state()
    return {"messages": state.get("a2a_messages", [])}


@app.get("/api/context")
def context() -> Dict[str, Any]:
    state = service.last_state()
    return state.get("repository_context", {})


@app.post("/api/analyze/documentation")
def analyze_documentation(request: RepositoryRequest) -> Dict[str, Any]:
    path = str(Path(request.repository_path or ".").resolve())
    return documentation_analyzer_tool(path)


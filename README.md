# OrbitOps AI

Autonomous DevMLSecOps Intelligence Platform Powered by GitLab Orbit.

OrbitOps AI is a production-style hackathon platform that reviews software delivery readiness before production deployment. It combines GitLab Orbit context, LangGraph-compatible multi-agent orchestration, A2A handoffs, MCP-style tools, a FastAPI backend, and an executive dashboard.

## Architecture

```text
GitLab Orbit Context
  -> Repository Context Layer
  -> LangGraph StateGraph
  -> Multi-Agent Hub
  -> Executive Dashboard
```

The backend runs nine agents:

- Repository Intelligence Agent
- Code Quality Agent
- Security Agent
- ML Governance Agent
- Documentation Agent
- CI/CD Agent
- Release Readiness Agent
- Engineering Risk Agent
- Executive Summary Agent

Each agent receives the shared `OrbitState`, updates its review section, sends an A2A handoff message, and contributes recommendations.

## Backend

FastAPI endpoints:

- `GET /`
- `GET /health`
- `GET /dashboard`
- `POST /api/analyze/repository`
- `POST /api/analyze/security`
- `POST /api/analyze/release`
- `POST /api/orbitops/run`
- `GET /api/a2a/messages`
- `GET /api/context`

Run locally:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Analyze the current repository:

```powershell
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/orbitops/run -ContentType 'application/json' -Body '{"repository_path":"."}'
```

## Frontend

The React dashboard provides:

- Repository, security, documentation, pipeline, release, and risk score cards
- Agent status
- A2A message stream
- GitLab Orbit context panel
- Executive summary and deployment recommendations
- Risk, security, and quality charts

Run locally:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`.

## Docker

```powershell
docker compose up --build
```

Backend: `http://127.0.0.1:8000`

Frontend: `http://127.0.0.1:5173`

## Configuration

Current hackathon mode works fully offline against a local repository path. Production integrations can be added behind the existing service contracts:

- GitLab Orbit APIs in `backend/services/mcp_tools.py`
- LangSmith tracing in `backend/services/langgraph_flow.py`
- LLM-backed analysis inside individual agents
- PostgreSQL persistence for run history and multi-repository support

## Testing

```powershell
pytest -q
python -m compileall backend
```

## Release Decision Model

The Release Readiness Agent gates production approval using security, code quality, documentation, and CI/CD signals. The Executive Summary Agent converts the aggregate result into `GO` or `NO-GO`.


# OrbitOps AI

## Tagline

Autonomous DevMLSecOps Intelligence Platform Powered by GitLab Orbit.

## Inspiration

Engineering teams ship through fragmented checks: code review, pipeline status, security scans, documentation review, ML governance, and release approval all live in separate systems. OrbitOps AI turns those signals into one autonomous readiness review before production deployment.

## What It Does

OrbitOps AI analyzes a repository and produces executive engineering intelligence:

- Repository health
- Code quality
- Secret and dependency posture
- ML governance risk
- Documentation readiness
- CI/CD health
- Release approval status
- Overall engineering risk
- Recommended deployment actions

## How We Built It

The backend uses FastAPI and a LangGraph-compatible StateGraph workflow. Each autonomous agent updates the shared OrbitState, then sends an A2A handoff message to the next agent. MCP-style tools provide repository, security, documentation, pipeline, release, and executive-report capabilities.

The frontend uses React, Vite, Recharts, and lucide-react to provide a dark enterprise dashboard inspired by GitLab, Datadog, Grafana, Linear, and GitHub Copilot.

## Architecture

GitLab Orbit context feeds the Repository Context Layer. A LangGraph StateGraph coordinates the Multi-Agent Hub. The Executive Dashboard presents release readiness, risk posture, A2A messages, and recommendations.

## Challenges

The main challenge was making the system impressive while still runnable in a hackathon environment without requiring live GitLab or LLM credentials. The solution is a clean offline mode with production integration points for GitLab Orbit APIs, LangSmith, LLM-backed reasoning, and persistent storage.

## Accomplishments

- Built a complete FastAPI multi-agent backend
- Implemented A2A handoff tracking
- Implemented MCP-style tool contracts
- Added LangGraph-compatible orchestration
- Built an executive dashboard with real API integration
- Added Docker, Compose, GitLab CI, demo script, and tests

## What's Next

- Live GitLab Orbit API integration
- GitLab merge request intelligence
- LangSmith trace visualization
- Executive PDF report export
- PostgreSQL run history
- Multi-repository portfolio risk view
- LLM-backed natural language repository analysis


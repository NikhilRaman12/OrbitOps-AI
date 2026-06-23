# Devpost Submission - OrbitOps AI

## Inspiration
As applications grow, modern DevSecOps pipelines face visual fragmentation and blind spots—particularly around Machine Learning (ML) deployment risk and dependency postures. Furthermore, security auditors and developers speak different languages. We wanted to build an autonomous agent team that acts as a release gatekeeper, reading GitLab Orbit context to produce a unified, readable Executive Release Readiness Report while maintaining full compliance transparency.

## What it does
**OrbitOps AI** is an autonomous DevMLSecOps intelligence platform powered by the GitLab Orbit context layer. It scans code repositories and evaluates:
1. **Repository Health**: Code structure, file size issues, and language statistics.
2. **Code Quality**: Functions exceeding maintainability thresholds and syntax smells.
3. **Security Posture**: Secret key patterns and insecure configuration (e.g. debug flags).
4. **Dependency Risks**: Risky packages and vulnerable manifest definitions.
5. **Documentation Readiness**: Essential setup, API, and deployment sections in READMEs.
6. **CI/CD Pipeline Integrity**: Checks for GitLab CI configs, Dockerfiles, and test suites.
7. **ML Governance Profile**: Heuristics for scikit-learn/pytorch/tensorflow and existence of model cards.

The system orchestrates **8 autonomous agents** using a LangGraph workflow. The agents communicate using an Agent-to-Agent (A2A) handoff protocol to exchange findings before the **Release Decision Agent** locks or approves the deployment gate. Finally, the **Executive Report Agent** compiles the findings into a dashboard-friendly summary.

## How we built it
* **Backend**: FastAPI web server with Python 3.12, orchestrating agents via a LangGraph `StateGraph`. We defined clear Pydantic schemas for typing safety.
* **Frontend**: A high-performance dashboard using React, Vite, Tailwind-like styling, Lucide icons, and Recharts for dynamic visual telemetry.
* **Context Layer**: GitLab Orbit integration tool that aggregates git status and project flags, falling back gracefully to offline telemetry when credentials are not configured.

## Challenges we overcame
* **State Synchronization**: Sharing data across 8 distinct agents within a TypedDict was solved by enforcing a clean, non-overlapping schema in `OrbitState`.
* **Agent Timeline Tracking**: Mapping A2A handoffs dynamically on a React frontend required a custom messaging timestamp log that models agent intents.

## Accomplishments that we're proud of
* Designing a highly responsive, modern dark-themed enterprise console (inspired by Grafana and GitLab) that renders real-time timeline streams.
* Creating a fully functional ML Governance checker that enforces model and dataset cards during production releases.

## What we learned
* Multi-agent flows work best when nodes have single-responsibility boundaries and use explicit contract handoffs rather than unstructured text chats.
* Seamless offline/demo fallback states are essential for smooth developer evaluations and hackathon judging.

## What's next for OrbitOps AI
* **Active Merge Request Remediation**: Implement GitLab Duo/Orbit automated MR comments to suggest code fixes directly in pipelines.
* **Enhanced ML Drift Tracking**: Integrating dynamic data-drift and model monitoring alerts directly inside GitLab issues.

## Technologies Used
* Python 3.12
* FastAPI
* LangGraph
* Pydantic V2
* React 18
* Vite
* Recharts
* Pytest
* GitLab CI/CD

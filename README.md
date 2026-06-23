# OrbitOps AI

> **Autonomous DevMLSecOps Intelligence Platform Powered by GitLab Orbit.**

---

## 📖 Table of Contents
1. [The Problem](#-the-problem)
2. [The Solution](#-the-solution)
3. [Why GitLab Orbit?](#-why-gitlab-orbit)
4. [Architecture & Workflow](#-architecture--workflow)
5. [API Endpoints](#-api-endpoints)
6. [Setup Instructions](#-setup-instructions)
7. [Demo Flow](#-demo-flow)
8. [Hackathon Alignment](#-hackathon-alignment)
9. [Future Roadmap](#-future-roadmap)
10. [License](#-license)

---

## 🚨 The Problem
Modern DevOps pipelines suffer from **visual fragmentation and compliance blind spots**. Standard linting and testing pipelines output thousands of raw log lines, but fail to answer simple, high-level business questions:
* *Is our codebase actually ready for a production release?*
* *Are there exposed secrets, risky CORS setups, or vulnerable dependency packages?*
* *If we are deploying Machine Learning (ML) features, do we have model lineage governance in place?*

Auditors, engineering managers, and DevSecOps engineers lack a unified, real-time readiness dashboard. Instead, they context-switch between five different scanners, leading to release delays or silent security exposures.

---

## 💡 The Solution
**OrbitOps AI** solves this by establishing a team of **8 cooperative, autonomous agents** orchestrated using **LangGraph**. The platform scans any repository, evaluates health, quality, secrets, dependencies, docs, pipelines, and ML governance, and produces a definitive **Release Gate Decision** (`APPROVED`, `APPROVED_WITH_WARNINGS`, or `BLOCKED`) alongside an **Executive Release Report**.

It leverages an **Agent-to-Agent (A2A) handoff protocol** where each specialist agent validates a specific domain, logs its intent, and passes the context downstream, culminating in a beautiful executive dashboard.

---

## 🌌 Why GitLab Orbit?
**GitLab Orbit** serves as our **Context Intelligence Layer**. Orbit provides critical context across issue boards, pipeline history, merge requests, and contributor activity. 

OrbitOps AI connects to this context via the `gitlab_orbit_context_tool`. In production environments, it polls live merge request metadata and project attributes to feed down to the Repository, Security, and Release agents, transforming static scan rules into dynamic context-aware deployment decisions.

---

## 🏗️ Architecture & Workflow

### Heuristic Orchestration Sequence

```text
       GitLab Orbit Context Layer (Signals, Project ID, Branch)
                     ↓
        Repository Context Agent (Health, Files, Languages)
                     ↓
        Security Agent (Secrets Scanner, Insecure Configs)
                     ↓
        Dependency Agent (Manifest Scanner, Risky Packages)
                     ↓
        Documentation Agent (README structure & section coverage)
                     ↓
        CI/CD Agent (GitLab CI, Docker, Compose, test folders)
                     ↓
        ML Governance Agent (Model indicators, Cards, lineage status)
                     ↓
        Release Decision Agent (Consolidates scores, gates APPROVED/BLOCKED)
                     ↓
        Executive Report Agent (Summarizes, lists actions, demo timeline)
                     ↓
        Executive Dark Theme Dashboard + JSON Response
```

### Agent Handoff Protocol
Agents communicate sequentially via structured state handoffs:
1. **Repository Context Agent** -> intent: `repository_context_ready` -> **Security Agent**
2. **Security Agent** -> intent: `security_review_ready` -> **Dependency Agent**
3. **Dependency Agent** -> intent: `dependency_review_ready` -> **Documentation Agent**
4. **Documentation Agent** -> intent: `documentation_review_ready` -> **CI/CD Agent**
5. **CI/CD Agent** -> intent: `cicd_review_ready` -> **ML Governance Agent**
6. **ML Governance Agent** -> intent: `ml_governance_ready` -> **Release Decision Agent**
7. **Release Decision Agent** -> intent: `release_decision_made` -> **Executive Report Agent**
8. **Executive Report Agent** -> intent: `executive_report_ready` -> **Dashboard**

---

## 🔌 API Endpoints

The backend is built on **FastAPI** and runs on port `8000`:
* `GET /api/health` - Simple health check returning `{"status": "healthy"}`.
* `GET /api/demo` - Returns a realistic, pre-compiled offline analysis result.
* `POST /api/analyze` - Triggers a real-time repository scan. Accepts:
  ```json
  {
    "repository_path": ".",
    "repository_url": "https://github.com/NikhilRaman12/OrbitOps-AI.git",
    "branch": "main"
  }
  ```
* `POST /api/orbitops/run` - Compatibility alias for the `/api/analyze` endpoint.
* `GET /api/report/{run_id}` - Fetches the complete multi-agent report for a specific run ID.

---

## 🛠️ Setup Instructions

### Prerequisites
* Python 3.11+
* Node.js 20+

### 1. Configuration (`.env`)
Create a `.env` file in the root folder (or copy `.env.example`):
```bash
cp .env.example .env
```
*Configure optional GitLab variables if checking live projects; otherwise, OrbitOps AI automatically operates in offline-fallback mode.*

### 2. Run Backend Locally
```bash
# Install dependencies
pip install -r requirements.txt

# Launch FastAPI server
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Run Frontend Locally
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:5173` in your browser.

### 4. Run via Docker Compose
To compile and spin up the complete stack:
```bash
docker compose up --build
```
* Backend: `http://localhost:8000`
* Frontend: `http://localhost:5173`

### 5. Running Tests
To run the automated backend endpoint and node checks:
```bash
pytest
```

---

## 🎬 Demo Flow
1. **Launch the Dashboard**: Access `http://localhost:5173`.
2. **Scan Local Repository**: Type `.` or a local repository path and click **Run Analysis**.
3. **Analyze Gate Decision**: Look at the overall **Readiness Score** (e.g. 81/100) and **Release Decision Badge** (e.g. APPROVED WITH WARNINGS).
4. **Audit Agent Timeline**: Expand the A2A timeline to see handoff messages between agents.
5. **Review Remediation Actions**: Check the color-coded action items list (e.g. security config fixes, documentation updates, dependency versions to bump).
6. **Graceful Offline Handling**: Stop the backend server and try to run. The frontend displays a warning banner and invites you to click **Load Offline Demo Telemetry** to preview the dashboard features seamlessly.

---

## 🏆 Hackathon Alignment
OrbitOps AI satisfies the requirements for the **GitLab Transcend Hackathon Showcase Track**:
1. **Fits GitLab Transcend**: Upgrades GitLab DevSecOps workflows into autonomous agentic pipelines.
2. **Working Agent & Flow**: 8 specialized agents cooperative chain orchestrated with LangGraph.
3. **Uses GitLab Orbit**: Incorporates a context layer using the `gitlab_orbit_context_tool` mimicking Duo chat inputs.
4. **Solves Real Problem**: Provides release gates and ML governance validation.
5. **Open Source**: MIT licensed.
6. **Demo Ready**: Includes complete [Devpost text](file:///c:/Users/Nikhil%20Raman%20K/OrbitOps-AI/docs/devpost.md) and [Video script](file:///c:/Users/Nikhil%20Raman%20K/OrbitOps-AI/docs/demo-script.md).

---

## 🚀 Future Roadmap
* **Duo Integration**: Create a custom GitLab Duo Agent plugin representing OrbitOps.
* **Auto-Remediation PRs**: Allow agents to push remediation commits (e.g. updating a requirements file or adding a missing model card) directly to a merge request in GitLab.

---

## 📄 License
This project is open-source and licensed under the [MIT License](file:///c:/Users/Nikhil%20Raman%20K/OrbitOps-AI/LICENSE).

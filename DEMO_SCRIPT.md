# OrbitOps AI Demo Script

## 1. Setup

```powershell
pip install -r requirements.txt
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

## 2. Open

Open `http://127.0.0.1:5173`.

## 3. Run Autonomous Review

Use repository path `.` and press Run.

Narration:

OrbitOps AI pulls local GitLab Orbit-style context, starts a LangGraph-compatible multi-agent workflow, and sends A2A handoffs across repository, quality, security, ML governance, documentation, CI/CD, release, risk, and executive agents.

## 4. Show Executive Intelligence

Point out:

- Overall risk
- Release readiness
- Executive summary
- Recommended actions
- Risk trend and score distribution

## 5. Show Engineering Detail

Switch to Engineering view.

Point out:

- A2A message stream
- GitLab Orbit context
- Agent completion status
- Security and pipeline findings

## 6. Close

OrbitOps turns fragmented DevSecOps and MLOps review into an autonomous production-readiness control plane for engineering leaders.


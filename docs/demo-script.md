# Demo Script - OrbitOps AI Video Walkthrough (3 Minutes)

## [0:00 - 0:20] The Problem
**Visual**: Zoomed-in look at standard GitLab CI yaml files and messy terminal warnings.
**Narrative**: 
> "Modern development velocity is faster than ever, but release gates remain slow. Engineering leads are constantly context-switching between dependency logs, security reports, model drift metrics, and documentation checklists. There is no single, consolidated readiness score, leading to skipped tests, exposed API secrets, or unmonitored ML models sneaking into production. We need an autonomous gatekeeper."

---

## [0:20 - 0:45] Introducing OrbitOps AI
**Visual**: Show OrbitOps AI brand title, transition to the premium dashboard.
**Narrative**: 
> "Introducing OrbitOps AI: an autonomous DevMLSecOps intelligence platform powered by GitLab Orbit. OrbitOps AI analyzes your repository's security, code smells, documentation, pipeline structures, and ML governance to produce a single, unified Release Readiness score. Under the hood, 8 cooperative agents collaborate in real-time to decide if your code is truly ready for deployment."

---

## [0:45 - 1:30] Live Dashboard Demo
**Visual**: Demonstrate pasting a repository path `.` and clicking **Run Analysis**. Watch the scores update and the timeline populate.
**Narrative**: 
> "Let's run a live analysis. By entering our local repository and triggering the run, the platform launches our agent team.
> Immediately, we get a visual overview: a Readiness Score of 81/100, and our release status is set to APPROVED WITH WARNINGS. 
> We can scan the scorecards: Repository Health at 88, Security Score at 92, and ML Governance flagged at 50 because we detected scikit-learn imports but found no model lineage cards."

---

## [1:30 - 2:15] Agent Workflow & GitLab Orbit Context
**Visual**: Scroll down to the A2A Orchestration Timeline and hover over the GitLab Orbit Context layer panel.
**Narrative**: 
> "Here is our Agent-to-Agent timeline. OrbitOps AI uses LangGraph. The Repository Context Agent reads repository metadata and passes the handoff to the Security Agent. The pipeline continues through Dependency, Documentation, CI/CD, and ML Governance agents.
> They communicate using typed handoff intents, feeding findings downstream. The GitLab Orbit Context Layer supplies real-time intelligence feeds, showing live integration status and project metadata directly from GitLab."

---

## [2:15 - 2:45] Release Recommendations
**Visual**: Focus on the Recommended Remediation Actions pane, highlighting the color-coded action items.
**Narrative**: 
> "In our actions list, we see precise, contextual suggestions grouped by urgency. The Dependency Agent tells us to upgrade `urllib3` to resolve known CVEs. The ML Governance Agent requests we add a `MODEL_CARD.md`. And our Security Agent flags a wide-open CORS policy in our main app. Correcting these issues and re-running automatically upgrades our Readiness Score and locks down vulnerabilities."

---

## [2:45 - 3:00] Closing Impact
**Visual**: Display OrbitOps AI logo, GitLab Transcend Hackathon text, and the MIT License.
**Narrative**: 
> "OrbitOps AI changes the release workflow from manual checks to autonomous, GitLab Orbit-powered verification. It is open source, lightweight, and ready to deploy. Deploy with confidence. Thank you!"

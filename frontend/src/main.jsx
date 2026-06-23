import React, { useMemo, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Activity,
  AlertTriangle,
  Bot,
  CheckCircle2,
  FileText,
  GitBranch,
  Play,
  ShieldCheck,
  Workflow
} from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";
import { runOrbitOps } from "./services/api";
import "./styles.css";

const sampleState = {
  repository_analysis: {
    repository_health: 82,
    source_files: 28,
    active_branches: 3,
    contributors: 6,
    languages: { ".py": 14, ".tsx": 7, ".yml": 4 }
  },
  security_review: { security_score: 88, critical_findings: [] },
  documentation_review: { documentation_score: 76, missing_sections: ["security"] },
  cicd_review: { pipeline_health: 70, pipeline_present: true },
  code_review: { quality_score: 84, critical_smells: [] },
  release_review: { release_ready: false, approval_status: "conditional_hold", blocking_issues: ["CI/CD controls are incomplete."] },
  risk_review: {
    overall_risk: "Medium",
    risk_score: 31,
    top_risks: ["pipeline score is 70"],
    score_breakdown: { repository: 82, code: 84, security: 88, documentation: 76, pipeline: 70, ml_governance: 74 }
  },
  executive_summary: {
    summary: "OrbitOps completed autonomous review. Overall risk is Medium with release decision NO-GO.",
    recommended_actions: ["Add release approval workflow.", "Add README security section."],
    release_decision: "NO-GO"
  },
  recommendations: [
    { area: "cicd", action: "Add GitLab CI stages for lint, tests, security scans, and release approval." },
    { area: "documentation", action: "Add README section for security." }
  ],
  a2a_messages: [
    { sender: "Repository Intelligence Agent", receiver: "Code Quality Agent", intent: "repository_context_ready" },
    { sender: "Code Quality Agent", receiver: "Security Agent", intent: "code_quality_ready" },
    { sender: "Security Agent", receiver: "ML Governance Agent", intent: "security_review_ready" },
    { sender: "Release Readiness Agent", receiver: "Engineering Risk Agent", intent: "release_review_ready" }
  ],
  repository_context: { provider: "gitlab-orbit", repository_url: "local-workspace", default_branch: "main" }
};

function metricCards(state) {
  return [
    {
      label: "Repository Health",
      value: state.repository_analysis?.repository_health ?? 0,
      icon: GitBranch,
      tone: "violet"
    },
    {
      label: "Security Score",
      value: state.security_review?.security_score ?? 0,
      icon: ShieldCheck,
      tone: "green"
    },
    {
      label: "Documentation",
      value: state.documentation_review?.documentation_score ?? 0,
      icon: FileText,
      tone: "amber"
    },
    {
      label: "Pipeline Health",
      value: state.cicd_review?.pipeline_health ?? 0,
      icon: Workflow,
      tone: "blue"
    },
    {
      label: "Release Readiness",
      value: state.release_review?.release_ready ? 100 : 42,
      display: state.release_review?.release_ready ? "Ready" : "Hold",
      icon: CheckCircle2,
      tone: state.release_review?.release_ready ? "green" : "red"
    },
    {
      label: "Overall Risk",
      value: state.risk_review?.risk_score ?? 0,
      display: state.risk_review?.overall_risk ?? "Unknown",
      icon: AlertTriangle,
      tone: "red"
    }
  ];
}

function App() {
  const [state, setState] = useState(sampleState);
  const [repoPath, setRepoPath] = useState(".");
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState("executive");
  const [error, setError] = useState("");

  const cards = useMemo(() => metricCards(state), [state]);
  const scoreData = Object.entries(state.risk_review?.score_breakdown ?? {}).map(([name, score]) => ({ name, score }));
  const trendData = [
    { name: "T-5", risk: 42 },
    { name: "T-4", risk: 38 },
    { name: "T-3", risk: 35 },
    { name: "T-2", risk: 33 },
    { name: "Now", risk: state.risk_review?.risk_score ?? 0 }
  ];
  const securityData = [
    { name: "Critical", value: state.security_review?.critical_findings?.length ?? 0, color: "#ef4444" },
    { name: "Clean", value: Math.max(1, 8 - (state.security_review?.critical_findings?.length ?? 0)), color: "#22c55e" }
  ];

  async function handleRun() {
    setLoading(true);
    setError("");
    try {
      const result = await runOrbitOps(repoPath);
      setState(result);
    } catch (err) {
      setError("Backend is unreachable. Showing embedded demo telemetry.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand">
          <div className="brandMark">O</div>
          <div>
            <h1>OrbitOps AI</h1>
            <p>Autonomous DevMLSecOps Intelligence Platform Powered by GitLab Orbit</p>
          </div>
        </div>
        <div className="toolbar">
          <div className="segmented" aria-label="View mode">
            <button className={mode === "executive" ? "active" : ""} onClick={() => setMode("executive")}>Executive</button>
            <button className={mode === "engineering" ? "active" : ""} onClick={() => setMode("engineering")}>Engineering</button>
          </div>
          <div className="repoInput">
            <input value={repoPath} onChange={(event) => setRepoPath(event.target.value)} aria-label="Repository path" />
            <button onClick={handleRun} disabled={loading} title="Run autonomous review">
              <Play size={16} />
              {loading ? "Running" : "Run"}
            </button>
          </div>
        </div>
      </header>

      {error && <div className="notice">{error}</div>}

      <section className="metricGrid">
        {cards.map((card) => {
          const Icon = card.icon;
          return (
            <article className={`metricCard ${card.tone}`} key={card.label}>
              <div className="metricHeader">
                <Icon size={18} />
                <span>{card.label}</span>
              </div>
              <strong>{card.display ?? card.value}</strong>
              <div className="meter"><span style={{ width: `${Math.min(100, card.value)}%` }} /></div>
            </article>
          );
        })}
      </section>

      <section className="contentGrid">
        <article className="panel wide">
          <div className="panelHeader">
            <h2>Executive Summary</h2>
            <span className={`decision ${state.executive_summary?.release_decision === "GO" ? "go" : "nogo"}`}>
              {state.executive_summary?.release_decision ?? "Pending"}
            </span>
          </div>
          <p className="summaryText">{state.executive_summary?.summary}</p>
          <div className="actionsList">
            {(state.executive_summary?.recommended_actions ?? state.recommendations?.map((item) => item.action) ?? []).slice(0, 5).map((item) => (
              <div className="actionItem" key={item}>
                <CheckCircle2 size={16} />
                <span>{item}</span>
              </div>
            ))}
          </div>
        </article>

        <article className="panel">
          <div className="panelHeader">
            <h2>Risk Trend</h2>
            <Activity size={18} />
          </div>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={trendData}>
              <CartesianGrid stroke="#263241" vertical={false} />
              <XAxis dataKey="name" stroke="#8793a3" />
              <YAxis stroke="#8793a3" />
              <Tooltip contentStyle={{ background: "#121926", border: "1px solid #334155" }} />
              <Line type="monotone" dataKey="risk" stroke="#f59e0b" strokeWidth={3} dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        </article>

        <article className="panel">
          <div className="panelHeader">
            <h2>Score Distribution</h2>
            <Bot size={18} />
          </div>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={scoreData}>
              <CartesianGrid stroke="#263241" vertical={false} />
              <XAxis dataKey="name" stroke="#8793a3" />
              <YAxis stroke="#8793a3" />
              <Tooltip contentStyle={{ background: "#121926", border: "1px solid #334155" }} />
              <Bar dataKey="score" radius={[5, 5, 0, 0]} fill="#8b5cf6" />
            </BarChart>
          </ResponsiveContainer>
        </article>

        <article className="panel">
          <div className="panelHeader">
            <h2>Security Findings</h2>
            <ShieldCheck size={18} />
          </div>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Pie data={securityData} dataKey="value" nameKey="name" innerRadius={54} outerRadius={82}>
                {securityData.map((entry) => <Cell key={entry.name} fill={entry.color} />)}
              </Pie>
              <Tooltip contentStyle={{ background: "#121926", border: "1px solid #334155" }} />
            </PieChart>
          </ResponsiveContainer>
        </article>

        <article className="panel">
          <div className="panelHeader">
            <h2>Agent Status</h2>
            <Bot size={18} />
          </div>
          <div className="agentList">
            {Object.entries(state.agent_status ?? {}).map(([agent, status]) => (
              <div className="agentRow" key={agent}>
                <span>{agent}</span>
                <b>{status}</b>
              </div>
            ))}
          </div>
        </article>

        <article className="panel wide">
          <div className="panelHeader">
            <h2>A2A Messages</h2>
            <Workflow size={18} />
          </div>
          <div className="messageStream">
            {(state.a2a_messages ?? []).map((message, index) => (
              <div className="message" key={message.id ?? `${message.sender}-${index}`}>
                <span>{message.sender}</span>
                <b>{message.intent}</b>
                <span>{message.receiver}</span>
              </div>
            ))}
          </div>
        </article>

        {mode === "engineering" && (
          <article className="panel wide">
            <div className="panelHeader">
              <h2>GitLab Orbit Context</h2>
              <GitBranch size={18} />
            </div>
            <pre className="contextBlock">{JSON.stringify(state.repository_context, null, 2)}</pre>
          </article>
        )}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);


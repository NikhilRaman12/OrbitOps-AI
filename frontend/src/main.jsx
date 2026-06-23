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
  Workflow,
  Cpu,
  Layers,
  CheckSquare,
  ShieldAlert,
  ArrowRight
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
import { runOrbitOps, getDemoTelemetry } from "./services/api";
import "./styles.css";

const sampleState = {
  run_id: "demo-run-uuid-1234",
  repository_context: { 
    provider: "gitlab-orbit", 
    repository_url: "local-workspace", 
    default_branch: "main",
    context_freshness: "live-local",
    integration_status: "offline-fallback",
    orbit_metadata: {
      project_id: "demo-project-id",
      api_endpoint: "https://gitlab.com/api/v4",
      duo_chat_enabled: True,
      context_tokens_analyzed: 4821
    }
  },
  repository_analysis: {
    repository_health: 82,
    source_files: 28,
    total_files: 35,
    active_branches: 3,
    contributors: 6,
    languages: { ".py": 14, ".tsx": 7, ".yml": 4 }
  },
  code_review: { quality_score: 84, critical_smells: [], recommendations: ["Optimize code loops in backend core."] },
  security_review: { security_score: 88, critical_findings: [], insecure_configs: [] },
  dependency_review: { dependency_score: 90, packages_count: 14, risky_dependencies: [] },
  documentation_review: { documentation_score: 76, missing_sections: ["security"] },
  cicd_review: { pipeline_health: 70, pipeline_present: true },
  ml_review: { governance_score: 100, ml_detected: false, frameworks: [], model_files: [], recommendations: [] },
  release_review: { release_ready: true, approval_status: "APPROVED_WITH_WARNINGS", readiness_score: 81, blocking_issues: [] },
  risk_review: {
    overall_risk: "Medium",
    risk_score: 19,
    top_risks: ["pipeline score is 70"],
    score_breakdown: { repository: 82, code: 84, security: 88, dependency: 90, documentation: 76, pipeline: 70, ml_governance: 100 }
  },
  executive_summary: {
    summary: "OrbitOps completed autonomous review. Overall risk is Medium with release decision APPROVED_WITH_WARNINGS.",
    recommended_actions: ["Add release approval workflow.", "Add README security section."],
    release_decision: "APPROVED_WITH_WARNINGS",
    explanation: "The project has an overall readiness score of 81/100. Deployment status is APPROVED_WITH_WARNINGS based on security and pipeline compliance."
  },
  recommendations: [
    { area: "cicd", action: "Add GitLab CI stages for lint, tests, security scans, and release approval." },
    { area: "documentation", action: "Add README section for security." }
  ],
  a2a_messages: [
    { id: "1", sender: "Repository Context Agent", receiver: "Security Agent", intent: "repository_context_ready", timestamp: "2026-06-23T18:00:00Z" },
    { id: "2", sender: "Security Agent", receiver: "Dependency Agent", intent: "security_review_ready", timestamp: "2026-06-23T18:00:02Z" },
    { id: "3", sender: "Dependency Agent", receiver: "Documentation Agent", intent: "dependency_review_ready", timestamp: "2026-06-23T18:00:04Z" },
    { id: "4", sender: "Documentation Agent", receiver: "CI/CD Agent", intent: "documentation_review_ready", timestamp: "2026-06-23T18:00:06Z" },
    { id: "5", sender: "CI/CD Agent", receiver: "ML Governance Agent", intent: "cicd_review_ready", timestamp: "2026-06-23T18:00:08Z" },
    { id: "6", sender: "ML Governance Agent", receiver: "Release Decision Agent", intent: "ml_governance_reviewed", timestamp: "2026-06-23T18:00:10Z" },
    { id: "7", sender: "Release Decision Agent", receiver: "Executive Report Agent", intent: "release_decision_made", timestamp: "2026-06-23T18:00:12Z" },
    { id: "8", sender: "Executive Report Agent", receiver: "Dashboard", intent: "executive_report_ready", timestamp: "2026-06-23T18:00:14Z" }
  ],
  agent_status: {
    "Repository Context Agent": "completed",
    "Security Agent": "completed",
    "Dependency Agent": "completed",
    "Documentation Agent": "completed",
    "CI/CD Agent": "completed",
    "ML Governance Agent": "completed",
    "Release Decision Agent": "completed",
    "Executive Report Agent": "completed"
  }
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
      label: "Dependency Posture",
      value: state.dependency_review?.dependency_score ?? 0,
      icon: Layers,
      tone: "blue"
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
      tone: "indigo"
    },
    {
      label: "ML Governance",
      value: state.ml_review?.governance_score ?? 0,
      icon: Cpu,
      tone: "cyan"
    }
  ];
}

function App() {
  const [state, setState] = useState(sampleState);
  const [repoPath, setRepoPath] = useState(".");
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState("executive");
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("overview");

  const cards = useMemo(() => metricCards(state), [state]);
  
  const scoreData = useMemo(() => {
    return Object.entries(state.risk_review?.score_breakdown ?? {}).map(([name, score]) => ({
      name: name.replace("_", " ").toUpperCase(),
      score
    }));
  }, [state]);

  const trendData = [
    { name: "Run-5", risk: 38 },
    { name: "Run-4", risk: 32 },
    { name: "Run-3", risk: 29 },
    { name: "Run-2", risk: 25 },
    { name: "Current", risk: state.risk_review?.risk_score ?? 0 }
  ];

  const pieData = useMemo(() => {
    const criticals = state.security_review?.critical_findings?.length ?? 0;
    const insecure = state.security_review?.insecure_configs?.length ?? 0;
    const riskyDeps = state.dependency_review?.risky_dependencies?.length ?? 0;
    
    const issues = criticals + insecure + riskyDeps;
    return [
      { name: "Exposures / Risks", value: issues, color: issues > 0 ? "#ef4444" : "#22c55e" },
      { name: "Healthy Controls", value: Math.max(1, 10 - issues), color: "#10b981" }
    ];
  }, [state]);

  async function handleRun() {
    setLoading(true);
    setError("");
    try {
      const result = await runOrbitOps(repoPath);
      setState(result);
    } catch (err) {
      setError("Backend is unreachable or failed. You can run in Offline Demo Mode below to preview telemetry.");
    } finally {
      setLoading(false);
    }
  }

  async function handleLoadDemo() {
    setLoading(true);
    setError("");
    try {
      const result = await getDemoTelemetry();
      setState(result);
    } catch (err) {
      setError("Could not load demo telemetry from backend. Showing local dashboard fallback instead.");
      setState(sampleState);
    } finally {
      setLoading(false);
    }
  }

  const decisionStatus = state.release_review?.approval_status ?? "BLOCKED";
  
  const statusConfig = {
    APPROVED: { color: "go", text: "APPROVED FOR DEPLOYMENT", icon: CheckCircle2 },
    APPROVED_WITH_WARNINGS: { color: "warning", text: "APPROVED WITH WARNINGS", icon: AlertTriangle },
    BLOCKED: { color: "nogo", text: "DEPLOYMENT BLOCKED", icon: ShieldAlert }
  };

  const currentStatus = statusConfig[decisionStatus] || statusConfig.BLOCKED;
  const StatusIcon = currentStatus.icon;

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand">
          <div className="brandMark">🚀</div>
          <div>
            <h1>OrbitOps AI</h1>
            <p>Autonomous DevMLSecOps Intelligence Platform Powered by GitLab Orbit</p>
          </div>
        </div>
        
        <div className="toolbar">
          <div className="segmented" aria-label="View mode">
            <button className={mode === "executive" ? "active" : ""} onClick={() => setMode("executive")}>Executive View</button>
            <button className={mode === "engineering" ? "active" : ""} onClick={() => setMode("engineering")}>Engineering View</button>
          </div>
          <div className="repoInput">
            <input 
              value={repoPath} 
              onChange={(event) => setRepoPath(event.target.value)} 
              placeholder="Repository path (e.g. .)"
              aria-label="Repository path" 
            />
            <button className="btn-run" onClick={handleRun} disabled={loading} title="Run autonomous review">
              <Play size={16} fill="currentColor" />
              {loading ? "Analyzing..." : "Run Analysis"}
            </button>
          </div>
        </div>
      </header>

      {error && (
        <div className="notice warning-banner">
          <div className="notice-content">
            <AlertTriangle size={20} className="notice-icon" />
            <span>{error}</span>
          </div>
          <button className="btn-demo-fallback" onClick={handleLoadDemo}>
            Load Offline Demo Telemetry
          </button>
        </div>
      )}

      {/* Main dashboard widgets */}
      <section className="dashboard-grid-summary">
        {/* Core Release Readiness Score */}
        <article className="panel score-main-card">
          <div className="score-radial">
            <div className="score-radial-inner">
              <span className="score-label">READINESS</span>
              <strong className="score-number">{state.release_review?.readiness_score ?? 0}</strong>
              <span className="score-total">/ 100</span>
            </div>
          </div>
          
          <div className="score-details">
            <h2>Release Decision Gate</h2>
            <div className={`status-badge ${currentStatus.color}`}>
              <StatusIcon size={16} />
              <span>{currentStatus.text}</span>
            </div>
            <p className="risk-level-tag">
              Overall Risk Exposure: <strong>{state.risk_review?.overall_risk ?? "Medium"} ({state.risk_review?.risk_score ?? 0}% Score)</strong>
            </p>
          </div>
        </article>

        {/* Executive Summary */}
        <article className="panel summary-main-card">
          <div className="panelHeader">
            <h2>Executive Analysis</h2>
            <span className="timestamp-badge">Run ID: {state.run_id ? state.run_id.substring(0, 13) : "Local-Run"}</span>
          </div>
          <p className="summaryText">{state.executive_summary?.summary}</p>
          <p className="explanationText">{state.executive_summary?.explanation}</p>
          
          {state.release_review?.blocking_issues && state.release_review.blocking_issues.length > 0 && (
            <div className="blockers-box">
              <h3 className="blocker-title">Release Blockers:</h3>
              <ul className="blockers-list">
                {state.release_review.blocking_issues.map((issue, idx) => (
                  <li key={idx} className="blocker-item">
                    <ShieldAlert size={14} />
                    <span>{issue}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </article>
      </section>

      {/* 6 Metric scorecards */}
      <section className="metricGrid">
        {cards.map((card) => {
          const Icon = card.icon;
          return (
            <article className={`metricCard ${card.tone}`} key={card.label}>
              <div className="metricHeader">
                <Icon size={18} />
                <span>{card.label}</span>
              </div>
              <div className="metric-body">
                <strong>{card.value}</strong>
                <span className="metric-limit">/100</span>
              </div>
              <div className="meter">
                <span style={{ width: `${Math.min(100, card.value)}%` }} />
              </div>
            </article>
          );
        })}
      </section>

      {/* Main sections split */}
      <section className="contentGrid">
        
        {/* Left column: agent flow and recommendations */}
        <div className="panel-col span-2">
          
          {/* Agent Status Monitor */}
          <article className="panel">
            <div className="panelHeader">
              <h2>Autonomous Agent Team Status</h2>
              <span className="badge-count">{Object.keys(state.agent_status ?? {}).length} Agents Active</span>
            </div>
            
            <div className="agent-grid">
              {Object.entries(state.agent_status ?? {}).map(([agent, status]) => {
                let scoreText = "N/A";
                if (agent.includes("Repository") && state.repository_analysis) {
                  scoreText = `${state.repository_analysis.repository_health}/100`;
                } else if (agent.includes("Security") && state.security_review) {
                  scoreText = `${state.security_review.security_score}/100`;
                } else if (agent.includes("Dependency") && state.dependency_review) {
                  scoreText = `${state.dependency_review.dependency_score}/100`;
                } else if (agent.includes("Documentation") && state.documentation_review) {
                  scoreText = `${state.documentation_review.documentation_score}/100`;
                } else if (agent.includes("CI/CD") && state.cicd_review) {
                  scoreText = `${state.cicd_review.pipeline_health}/100`;
                } else if (agent.includes("ML") && state.ml_review) {
                  scoreText = `${state.ml_review.governance_score}/100`;
                } else if (agent.includes("Release") && state.release_review) {
                  scoreText = `${state.release_review.readiness_score}/100`;
                } else if (agent.includes("Executive") && state.risk_review) {
                  scoreText = `${100 - state.risk_review.risk_score}/100`;
                }
                
                return (
                  <div className="agent-badge-card" key={agent}>
                    <div className="agent-badge-top">
                      <span className={`status-dot ${status}`} />
                      <h3>{agent}</h3>
                    </div>
                    <div className="agent-badge-bottom">
                      <span className="agent-status-label">{status.toUpperCase()}</span>
                      <span className="agent-score-value">{scoreText}</span>
                    </div>
                  </div>
                );
              })}
            </div>
          </article>

          {/* Timeline and A2A handoffs */}
          <article className="panel">
            <div className="panelHeader">
              <h2>Agent-to-Agent (A2A) Orchestration Timeline</h2>
              <Workflow size={18} className="icon-header-accent" />
            </div>
            <div className="timeline-flow">
              {(state.a2a_messages ?? []).map((message, index) => (
                <div className="timeline-node" key={message.id ?? `${message.sender}-${index}`}>
                  <div className="timeline-connector" />
                  <div className="timeline-icon-box">
                    <ArrowRight size={14} />
                  </div>
                  <div className="timeline-content-card">
                    <div className="timeline-content-header">
                      <span className="timeline-sender">{message.sender}</span>
                      <span className="timeline-intent-tag">{message.intent}</span>
                      <span className="timeline-receiver">{message.receiver}</span>
                    </div>
                    <span className="timeline-time">{new Date(message.timestamp).toLocaleTimeString()}</span>
                  </div>
                </div>
              ))}
            </div>
          </article>

          {/* Recommended actions list */}
          <article className="panel">
            <div className="panelHeader">
              <h2>Recommended Remediation Actions</h2>
              <CheckSquare size={18} className="icon-header-accent" />
            </div>
            
            <div className="actionsList">
              {(state.executive_summary?.recommended_actions ?? state.recommendations?.map((item) => item.action) ?? []).map((item, index) => {
                let area = "General";
                if (typeof item === 'object') {
                  area = item.area || "General";
                  item = item.action;
                } else {
                  // Heuristics to find area
                  if (item.toLowerCase().includes("secret") || item.toLowerCase().includes("cors")) area = "security";
                  else if (item.toLowerCase().includes("readme") || item.toLowerCase().includes("document")) area = "documentation";
                  else if (item.toLowerCase().includes("upgrade") || item.toLowerCase().includes("package")) area = "dependency";
                  else if (item.toLowerCase().includes("ci") || item.toLowerCase().includes("docker")) area = "cicd";
                  else if (item.toLowerCase().includes("model") || item.toLowerCase().includes("dataset")) area = "ml_governance";
                }
                
                return (
                  <div className={`actionItem border-${area}`} key={index}>
                    <CheckCircle2 size={16} className={`action-icon-${area}`} />
                    <div className="action-text-box">
                      <span className="action-tag">{area.replace("_", " ").toUpperCase()}</span>
                      <p className="action-msg">{item}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </article>
        </div>

        {/* Right column: charts, context */}
        <div className="panel-col">
          
          {/* Risk Trend Chart */}
          <article className="panel">
            <div className="panelHeader">
              <h2>Engineering Risk Trend</h2>
              <Activity size={18} />
            </div>
            <ResponsiveContainer width="100%" height={200}>
              <LineChart data={trendData}>
                <CartesianGrid stroke="#263241" vertical={false} />
                <XAxis dataKey="name" stroke="#8793a3" />
                <YAxis stroke="#8793a3" domain={[0, 100]} />
                <Tooltip contentStyle={{ background: "#121926", border: "1px solid #334155" }} />
                <Line type="monotone" dataKey="risk" stroke="#f59e0b" strokeWidth={3} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </article>

          {/* Score distribution */}
          <article className="panel">
            <div className="panelHeader">
              <h2>Score Breakdown</h2>
              <Bot size={18} />
            </div>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={scoreData}>
                <CartesianGrid stroke="#263241" vertical={false} />
                <XAxis dataKey="name" stroke="#8793a3" tick={{ fontSize: 10 }} />
                <YAxis stroke="#8793a3" domain={[0, 100]} />
                <Tooltip contentStyle={{ background: "#121926", border: "1px solid #334155" }} />
                <Bar dataKey="score" radius={[4, 4, 0, 0]}>
                  {scoreData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.score >= 80 ? "#10b981" : entry.score >= 65 ? "#f59e0b" : "#ef4444"} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </article>

          {/* Security & Vulnerability components chart */}
          <article className="panel">
            <div className="panelHeader">
              <h2>Vulnerability Exposure Profile</h2>
              <ShieldCheck size={18} />
            </div>
            <div className="pie-container">
              <ResponsiveContainer width="100%" height={180}>
                <PieChart>
                  <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={48} outerRadius={68} paddingAngle={4}>
                    {pieData.map((entry, index) => <Cell key={`cell-${index}`} fill={entry.color} />)}
                  </Pie>
                  <Tooltip contentStyle={{ background: "#121926", border: "1px solid #334155" }} />
                </PieChart>
              </ResponsiveContainer>
              <div className="pie-legends">
                {pieData.map((entry, index) => (
                  <div className="pie-legend-item" key={index}>
                    <span className="legend-dot" style={{ backgroundColor: entry.color }} />
                    <span className="legend-label">{entry.name}: {entry.value}</span>
                  </div>
                ))}
              </div>
            </div>
          </article>

          {/* GitLab Orbit Context signals */}
          <article className="panel">
            <div className="panelHeader">
              <h2>GitLab Orbit Context Layer</h2>
              <GitBranch size={18} />
            </div>
            {mode === "engineering" ? (
              <pre className="contextBlock">{JSON.stringify(state.repository_context, null, 2)}</pre>
            ) : (
              <div className="context-brief-grid">
                <div className="context-brief-row">
                  <span>Intelligence Provider:</span>
                  <b>{state.repository_context?.provider ?? "gitlab-orbit"}</b>
                </div>
                <div className="context-brief-row">
                  <span>Freshness:</span>
                  <b>{state.repository_context?.context_freshness ?? "live-local"}</b>
                </div>
                <div className="context-brief-row">
                  <span>Integration Mode:</span>
                  <span className={`status-text-${state.repository_context?.integration_status === 'active' ? 'active' : 'offline'}`}>
                    {(state.repository_context?.integration_status ?? 'offline-fallback').toUpperCase()}
                  </span>
                </div>
                <div className="context-brief-row">
                  <span>Duo Chat Context:</span>
                  <b>{state.repository_context?.orbit_metadata?.duo_chat_enabled ? "ENABLED" : "DISABLED"}</b>
                </div>
                <div className="context-brief-row">
                  <span>Tokens Analyzed:</span>
                  <b>{state.repository_context?.orbit_metadata?.context_tokens_analyzed ?? 0}</b>
                </div>
              </div>
            )}
          </article>
        </div>

      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);

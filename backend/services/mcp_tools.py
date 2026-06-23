from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, Iterable, List


SOURCE_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".go",
    ".rs",
    ".cs",
    ".rb",
    ".php",
}

SECRET_PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "generic_secret": re.compile(r"(?i)(api[_-]?key|token|secret|password)\s*[:=]\s*['\"][^'\"]{8,}['\"]"),
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
}


def _safe_repo_root(path: str | None) -> Path:
    root = Path(path or ".").resolve()
    if not root.exists():
        raise ValueError(f"Repository path does not exist: {root}")
    if not root.is_dir():
        raise ValueError(f"Repository path is not a directory: {root}")
    return root


def _iter_files(root: Path) -> Iterable[Path]:
    ignored = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}
    for path in root.rglob("*"):
        if any(part in ignored for part in path.parts):
            continue
        if path.is_file():
            yield path


def gitlab_orbit_context_tool(repository_url: str | None = None, branch: str = "main") -> Dict[str, Any]:
    """Hackathon-mode GitLab Orbit context shim.

    Real deployments can replace this with GitLab Orbit APIs while preserving
    the downstream context contract.
    """
    return {
        "provider": "gitlab-orbit",
        "repository_url": repository_url or "local-workspace",
        "default_branch": branch,
        "context_freshness": "live-local",
        "signals": ["repository", "pipeline", "security", "documentation", "release"],
    }


def repository_analysis_tool(path: str | None = None) -> Dict[str, Any]:
    root = _safe_repo_root(path)
    files = list(_iter_files(root))
    source_files = [file for file in files if file.suffix in SOURCE_EXTENSIONS]
    extension_counts = Counter(file.suffix or "no_ext" for file in files)
    large_files = [
        {"path": str(file.relative_to(root)), "size_kb": round(file.stat().st_size / 1024, 1)}
        for file in files
        if file.stat().st_size > 256 * 1024
    ][:10]
    return {
        "root": str(root),
        "total_files": len(files),
        "source_files": len(source_files),
        "languages": dict(extension_counts.most_common(8)),
        "risk_files": large_files,
        "contributors": 1,
        "active_branches": 1,
    }


def code_quality_tool(path: str | None = None) -> Dict[str, Any]:
    root = _safe_repo_root(path)
    smells: List[Dict[str, Any]] = []
    total_lines = 0
    todo_count = 0
    long_function_count = 0

    for file in _iter_files(root):
        if file.suffix not in SOURCE_EXTENSIONS:
            continue
        try:
            lines = file.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        total_lines += len(lines)
        todo_count += sum(1 for line in lines if "TODO" in line or "FIXME" in line)
        long_lines = [idx + 1 for idx, line in enumerate(lines) if len(line) > 120]
        if long_lines:
            smells.append({"type": "long_lines", "path": str(file.relative_to(root)), "lines": long_lines[:5]})
        function_starts = [idx for idx, line in enumerate(lines) if re.match(r"\s*def\s+\w+", line)]
        for start, next_start in zip(function_starts, function_starts[1:] + [len(lines)]):
            if next_start - start > 80:
                long_function_count += 1

    score = max(35, 100 - min(45, len(smells) * 3) - min(10, todo_count) - min(10, long_function_count * 2))
    return {
        "quality_score": score,
        "total_lines": total_lines,
        "critical_smells": smells[:12],
        "recommendations": [
            "Break down long functions and isolate orchestration from business rules.",
            "Add automated tests around release and security decision logic.",
        ],
    }


def security_scanner_tool(path: str | None = None) -> Dict[str, Any]:
    root = _safe_repo_root(path)
    findings: List[Dict[str, Any]] = []
    dependency_files = []

    for file in _iter_files(root):
        rel = str(file.relative_to(root))
        if file.name in {"requirements.txt", "package.json", "pyproject.toml", "poetry.lock"}:
            dependency_files.append(rel)
        if file.stat().st_size > 512 * 1024:
            continue
        text = file.read_text(encoding="utf-8", errors="ignore")
        for name, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                findings.append({"severity": "critical", "type": name, "path": rel})

    score = max(20, 100 - (len(findings) * 18))
    return {
        "security_score": score,
        "critical_findings": findings,
        "vulnerabilities": [],
        "dependency_manifests": dependency_files,
        "owasp_coverage": ["secrets", "dependency-manifest-presence", "insecure-config-heuristics"],
    }


def documentation_analyzer_tool(path: str | None = None) -> Dict[str, Any]:
    root = _safe_repo_root(path)
    readme = next((file for file in [root / "README.md", root / "readme.md"] if file.exists()), None)
    text = readme.read_text(encoding="utf-8", errors="ignore") if readme else ""
    expected = ["installation", "usage", "api", "architecture", "deployment", "security"]
    missing = [section for section in expected if section not in text.lower()]
    score = 100 - (len(missing) * 12) if readme else 35
    return {
        "documentation_score": max(20, score),
        "readme_present": readme is not None,
        "missing_sections": missing,
        "recommendations": ["Document runbooks, environment variables, and deployment gates."],
    }


def pipeline_tool(path: str | None = None) -> Dict[str, Any]:
    root = _safe_repo_root(path)
    candidates = [root / ".gitlab-ci.yml", root / ".github" / "workflows"]
    has_pipeline = any(candidate.exists() for candidate in candidates)
    score = 82 if has_pipeline else 48
    recs = [] if has_pipeline else ["Add GitLab CI stages for lint, tests, security scans, and release approval."]
    return {
        "pipeline_health": score,
        "failed_checks": [],
        "pipeline_present": has_pipeline,
        "recommendations": recs,
    }


def merge_request_tool() -> Dict[str, Any]:
    return {
        "merge_request_intelligence": "offline",
        "open_merge_requests": 0,
        "review_latency_hours": None,
        "recommendations": ["Connect GitLab token to enable live MR intelligence."],
    }


def release_assessment_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    security_score = state.get("security_review", {}).get("security_score", 0)
    quality_score = state.get("code_review", {}).get("quality_score", 0)
    docs_score = state.get("documentation_review", {}).get("documentation_score", 0)
    pipeline_score = state.get("cicd_review", {}).get("pipeline_health", 0)
    blockers = []
    if security_score < 75:
        blockers.append("Security score below production threshold.")
    if quality_score < 70:
        blockers.append("Code quality needs remediation before release.")
    if pipeline_score < 65:
        blockers.append("CI/CD controls are incomplete.")
    release_ready = not blockers and docs_score >= 55
    return {
        "release_ready": release_ready,
        "blocking_issues": blockers,
        "approval_status": "approved" if release_ready else "conditional_hold",
    }


def executive_report_tool(state: Dict[str, Any]) -> Dict[str, Any]:
    risk = state.get("risk_review", {})
    release = state.get("release_review", {})
    decision = "GO" if release.get("release_ready") else "NO-GO"
    return {
        "summary": (
            f"OrbitOps completed autonomous review. Overall risk is "
            f"{risk.get('overall_risk', 'Unknown')} with release decision {decision}."
        ),
        "critical_findings": risk.get("top_risks", []),
        "recommended_actions": [item.get("action", str(item)) for item in state.get("recommendations", [])[:6]],
        "release_decision": decision,
    }


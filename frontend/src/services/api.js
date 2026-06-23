const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "";

export async function runOrbitOps(repositoryPath = ".") {
  const response = await fetch(`${API_BASE}/api/orbitops/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ repository_path: repositoryPath })
  });
  if (!response.ok) {
    throw new Error(`OrbitOps API failed with ${response.status}`);
  }
  return response.json();
}

export async function getDemoTelemetry() {
  const response = await fetch(`${API_BASE}/api/demo`, {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  });
  if (!response.ok) {
    throw new Error(`OrbitOps Demo API failed with ${response.status}`);
  }
  return response.json();
}

export async function getReport(runId) {
  const response = await fetch(`${API_BASE}/api/report/${runId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  });
  if (!response.ok) {
    throw new Error(`OrbitOps Report API failed with ${response.status}`);
  }
  return response.json();
}

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

async function unwrap(res) {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `request failed with ${res.status}`);
  }
  return res.json();
}

export function listDocuments() {
  return fetch(`${API_BASE}/api/documents`).then(unwrap);
}

export function uploadDocument(file) {
  const form = new FormData();
  form.append("file", file);
  return fetch(`${API_BASE}/api/documents`, { method: "POST", body: form }).then(unwrap);
}

export function sendMessage(question, conversationId) {
  return fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, conversation_id: conversationId }),
  }).then(unwrap);
}

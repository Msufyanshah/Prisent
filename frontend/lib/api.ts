import type { PersonaResponse, PostResponse, GenerationJob } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("prisent_token");
}

export function setToken(token: string) {
  localStorage.setItem("prisent_token", token);
}

export function clearToken() {
  localStorage.removeItem("prisent_token");
}

export class ApiError extends Error {
  constructor(public status: number, public code: string, message: string) {
    super(message);
  }
}

async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> || {})
  };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${API_URL}${path}`, { ...options, headers });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new ApiError(res.status, body.detail?.code || "UNKNOWN", body.detail?.message || res.statusText);
  }
  return res.json();
}

export const api = {
  register: (email: string, password: string, name: string) =>
    apiFetch<{ token: string }>("/auth/register", {
      method: "POST", body: JSON.stringify({ email, password, name })
    }),
  login: (email: string, password: string) =>
    apiFetch<{ token: string }>("/auth/login", {
      method: "POST", body: JSON.stringify({ email, password })
    }),
  getPersona: () => apiFetch<PersonaResponse>("/persona"),
  savePersona: (data: Partial<PersonaResponse>) =>
    apiFetch<PersonaResponse>("/persona", { method: "POST", body: JSON.stringify(data) }),
  triggerGeneration: () =>
    apiFetch<{ job_id: string }>("/generate", { method: "POST" }),
  pollGeneration: (jobId: string) =>
    apiFetch<GenerationJob>(`/generate/${jobId}`),
  listPosts: (status?: string) =>
    apiFetch<PostResponse[]>(`/posts${status ? `?status_filter=${status}` : ""}`),
  approvePost: (id: string, scheduledAt: string) =>
    apiFetch<PostResponse>(`/posts/${id}/approve`, { method: "POST", body: JSON.stringify({ scheduled_at: scheduledAt }) }),
  publishNow: (id: string) =>
    apiFetch<PostResponse>(`/posts/${id}/publish-now`, { method: "POST" }),
};

"use client";
import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";
import type { PersonaResponse } from "@/lib/types";

const TONE_OPTIONS = ["Authoritative & Technical", "Conversational", "Bold & Opinionated", "Storytelling"];
const GOAL_OPTIONS = ["Thought Leadership", "Grow Followers", "Get Clients", "Build Authority"];
const FREQ_OPTIONS = ["daily", "3x per week", "2x per week", "weekly"];

export default function SettingsPage() {
  const [form, setForm] = useState<Partial<PersonaResponse>>({
    name: "Jane Doe",
    headline: "Principal AI Engineer",
    niche: "B2B SaaS Architecture & Machine Learning",
    content_pillars: ["System Design", "AI Ethics"],
    target_audience: "Senior developers and tech leads",
    content_goal: "grow_followers",
    posting_frequency: "3x_week",
    tone: "professional",
    avoid_topics: [],
    unique_differentiator: "Focus on concrete code examples and measurable performance metrics rather than theoretical high-level concepts."
  });
  const [newPillar, setNewPillar] = useState("");
  const [addingPillar, setAddingPillar] = useState(false);
  const [statusText, setStatusText] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [liStatus, setLiStatus] = useState<{ connected: boolean; linkedin_name: string | null }>({ connected: false, linkedin_name: null });
  const [liLoading, setLiLoading] = useState(false);

  useEffect(() => {
    // Check if redirect has error query params
    if (typeof window !== "undefined") {
      const params = new URLSearchParams(window.location.search);
      const oauthError = params.get("error");
      if (oauthError) {
        setError(oauthError);
      }
    }

    api.getPersona()
      .then(p => {
        if (p) setForm(prev => ({ ...prev, ...p, tone: p.tone || "professional" }));
      })
      .catch(() => {});

    async function loadStatus() {
      try {
        const status = await api.getLinkedInStatus();
        setLiStatus(status);
      } catch (e) {
        console.error("Failed to load LinkedIn status:", e);
      }
    }
    loadStatus();
  }, []);

  async function handleConnect() {
    setLiLoading(true);
    try {
      const res = await api.getLinkedInConnectUrl();
      if (res.redirect_url) {
        window.location.href = res.redirect_url;
      }
    } catch (e) {
      console.error("Failed to get connection url:", e);
      setError("Failed to initiate LinkedIn connection.");
    } finally {
      setLiLoading(false);
    }
  }

  async function handleDisconnect() {
    setLiLoading(true);
    try {
      await api.disconnectLinkedIn();
      setLiStatus({ connected: false, linkedin_name: null });
      setStatusText("LinkedIn disconnected.");
    } catch (e) {
      console.error("Failed to disconnect LinkedIn:", e);
      setError("Failed to disconnect LinkedIn.");
    } finally {
      setLiLoading(false);
    }
  }

  async function handleSave(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setStatusText("");
    setLoading(true);
    try {
      const payload = {
        name: form.name || "",
        headline: form.headline || "",
        niche: form.niche || "",
        content_pillars: form.content_pillars || [],
        tone: form.tone || "professional",
        target_audience: form.target_audience || "",
        content_goal: form.content_goal || "grow_followers",
        posting_frequency: form.posting_frequency || "3x_week",
        avoid_topics: form.avoid_topics || [],
        unique_differentiator: form.unique_differentiator || ""
      };
      await api.savePersona(payload);
      const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      setStatusText(`Saved - ${time}`);
    } catch (e) {
      if (e instanceof ApiError) setError(e.message);
      else setError("Failed to save changes.");
    } finally {
      setLoading(false);
    }
  }

  function removePillar(p: string) {
    setForm(prev => ({
      ...prev,
      content_pillars: (prev.content_pillars || []).filter(item => item !== p)
    }));
  }

  function addPillar() {
    if (!newPillar.trim()) return;
    setForm(prev => ({
      ...prev,
      content_pillars: [...(prev.content_pillars || []), newPillar.trim()].slice(0, 3)
    }));
    setNewPillar("");
    setAddingPillar(false);
  }

  return (
    <div className="p-6 bg-background min-h-screen text-textPrimary max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-medium tracking-tight">Settings</h1>
        <p className="text-sm text-textMuted">Configure the identity and strategy behind your generated content</p>
      </div>

      <form onSubmit={handleSave} className="space-y-6 border border-borderMuted bg-surface p-6 rounded-container">
        
        {/* IDENTITY SECTION */}
        <div className="space-y-4">
          <h2 className="text-xs font-mono font-medium tracking-wider text-textMuted uppercase border-b border-borderMuted/30 pb-1">Identity</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-mono text-textMuted uppercase mb-1">Full Name</label>
              <input
                value={form.name || ""}
                onChange={e => setForm({ ...form, name: e.target.value })}
                className="w-full rounded-interactive border border-borderMuted bg-background px-3 py-2 text-sm text-textPrimary focus:border-accent focus:outline-none"
                required
              />
            </div>
            <div>
              <label className="block text-xs font-mono text-textMuted uppercase mb-1">Professional Headline</label>
              <input
                value={form.headline || ""}
                onChange={e => setForm({ ...form, headline: e.target.value })}
                className="w-full rounded-interactive border border-borderMuted bg-background px-3 py-2 text-sm text-textPrimary focus:border-accent focus:outline-none"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-mono text-textMuted uppercase mb-1">Primary Niche / Domain</label>
            <input
              value={form.niche || ""}
              onChange={e => setForm({ ...form, niche: e.target.value })}
              className="w-full rounded-interactive border border-borderMuted bg-background px-3 py-2 text-sm text-textPrimary focus:border-accent focus:outline-none"
              required
            />
          </div>
        </div>

        {/* CONTENT STRATEGY SECTION */}
        <div className="space-y-4">
          <h2 className="text-xs font-mono font-medium tracking-wider text-textMuted uppercase border-b border-borderMuted/30 pb-1">Content Strategy</h2>
          
          <div>
            <label className="block text-xs font-mono text-textMuted uppercase mb-2">Content Pillars (Max 3)</label>
            <div className="flex flex-wrap gap-2 items-center">
              {(form.content_pillars || []).map(pillar => (
                <span
                  key={pillar}
                  className="inline-flex items-center space-x-1.5 px-2.5 py-1 border border-borderMuted bg-background text-xs text-textPrimary rounded-interactive font-mono"
                >
                  <span>{pillar}</span>
                  <button
                    type="button"
                    onClick={() => removePillar(pillar)}
                    className="text-textMuted hover:text-danger"
                  >
                    ×
                  </button>
                </span>
              ))}

              {addingPillar ? (
                <div className="flex items-center space-x-1">
                  <input
                    value={newPillar}
                    onChange={e => setNewPillar(e.target.value)}
                    className="border border-borderMuted bg-background px-2 py-0.5 text-xs text-textPrimary focus:outline-none rounded-interactive"
                    placeholder="New pillar..."
                    autoFocus
                  />
                  <button
                    type="button"
                    onClick={addPillar}
                    className="text-xs text-accent px-1.5 py-0.5 border border-borderMuted hover:bg-borderMuted/30 rounded-interactive"
                  >
                    Add
                  </button>
                </div>
              ) : (
                (form.content_pillars || []).length < 3 && (
                  <button
                    type="button"
                    onClick={() => setAddingPillar(true)}
                    className="text-xs text-textMuted hover:text-accent border border-borderMuted border-dashed px-2.5 py-1 rounded-interactive font-mono"
                  >
                    + Add pillar...
                  </button>
                )
              )}
            </div>
          </div>

          <div>
            <label className="block text-xs font-mono text-textMuted uppercase mb-1">Target Audience</label>
            <input
              value={form.target_audience || ""}
              onChange={e => setForm({ ...form, target_audience: e.target.value })}
              className="w-full rounded-interactive border border-borderMuted bg-background px-3 py-2 text-sm text-textPrimary focus:border-accent focus:outline-none"
              required
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-mono text-textMuted uppercase mb-1">Primary Goal</label>
              <select
                value={form.content_goal || "grow_followers"}
                onChange={e => setForm({ ...form, content_goal: e.target.value as any })}
                className="w-full rounded-interactive border border-borderMuted bg-background px-3 py-2 text-sm text-textPrimary focus:border-accent focus:outline-none font-mono"
              >
                <option value="grow_followers">Thought Leadership</option>
                <option value="get_clients">Get Clients</option>
                <option value="build_authority">Build Authority</option>
                <option value="network">Network</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-mono text-textMuted uppercase mb-1">Posting Frequency</label>
              <select
                value={form.posting_frequency || "3x_week"}
                onChange={e => setForm({ ...form, posting_frequency: e.target.value as any })}
                className="w-full rounded-interactive border border-borderMuted bg-background px-3 py-2 text-sm text-textPrimary focus:border-accent focus:outline-none font-mono"
              >
                <option value="daily">Daily</option>
                <option value="3x_week">3x per week</option>
                <option value="2x_week">2x per week</option>
                <option value="weekly">Weekly</option>
              </select>
            </div>
          </div>
        </div>

        {/* VOICE SECTION */}
        <div className="space-y-4">
          <h2 className="text-xs font-mono font-medium tracking-wider text-textMuted uppercase border-b border-borderMuted/30 pb-1">Voice</h2>
          
          <div>
            <label className="block text-xs font-mono text-textMuted uppercase mb-1">Base Tone</label>
            <select
              value={form.tone || "professional"}
              onChange={e => setForm({ ...form, tone: e.target.value as any })}
              className="w-full rounded-interactive border border-borderMuted bg-background px-3 py-2 text-sm text-textPrimary focus:border-accent focus:outline-none font-mono"
            >
              <option value="professional">Authoritative & Technical</option>
              <option value="conversational">Conversational</option>
              <option value="bold">Bold & Opinionated</option>
              <option value="storytelling">Storytelling</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-mono text-textMuted uppercase mb-1">Unique Differentiator</label>
            <textarea
              value={form.unique_differentiator || ""}
              onChange={e => setForm({ ...form, unique_differentiator: e.target.value })}
              className="w-full h-24 rounded-interactive border border-borderMuted bg-background p-3 text-sm text-textPrimary leading-relaxed focus:border-accent focus:outline-none"
              required
            />
          </div>
        </div>

        {/* ERROR MESSAGE DISPLAY */}
        {error && (
          <div className="text-xs text-danger font-mono border border-danger/25 bg-danger/5 p-2 rounded-interactive">
            [ERR] {error}
          </div>
        )}

        {/* BOTTOM FORM BAR */}
        <div className="flex justify-end items-center space-x-4 border-t border-borderMuted/30 pt-4">
          {statusText && (
            <span className="text-xs font-mono text-success">
              [OK] {statusText}
            </span>
          )}
          <button
            type="button"
            className="px-4 py-2 border border-borderMuted rounded-interactive text-xs font-medium hover:bg-borderMuted/30 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 rounded-interactive bg-accent text-xs font-medium text-background hover:bg-accent-hover transition-colors disabled:opacity-40"
          >
            {loading ? "Saving..." : "Save changes"}
          </button>
        </div>

      </form>

      {/* LINKEDIN CONNECTION CARD */}
      <div className="border border-borderMuted bg-surface p-6 rounded-container space-y-4">
        <h2 className="text-xs font-mono font-medium tracking-wider text-textMuted uppercase border-b border-borderMuted/30 pb-1">Integrations</h2>
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center bg-background border border-borderMuted p-4 rounded-interactive gap-4">
          <div className="space-y-1">
            <div className="text-sm font-medium text-textPrimary">LinkedIn Integration</div>
            <div className="text-xs text-textMuted font-mono">
              {liStatus.connected 
                ? `[CONNECTED] Active session for ${liStatus.linkedin_name}`
                : "[DISCONNECTED] Standby. Authorization required to publish."
              }
            </div>
          </div>
          <div>
            {liStatus.connected ? (
              <button
                type="button"
                onClick={handleDisconnect}
                disabled={liLoading}
                className="px-4 py-2 rounded-interactive border border-red-500 text-red-500 text-xs font-mono hover:bg-red-500/5 transition-colors disabled:opacity-40"
              >
                Disconnect
              </button>
            ) : (
              <button
                type="button"
                onClick={handleConnect}
                disabled={liLoading}
                className="px-4 py-2 rounded-interactive bg-accent text-background text-xs font-mono font-bold hover:bg-accent-hover transition-colors disabled:opacity-40"
              >
                Connect LinkedIn
              </button>
            )}
          </div>
      </div>
    </div>
  </div>
  );
}

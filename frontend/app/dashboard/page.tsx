"use client";
import { useGenerationPoll } from "@/hooks/useGenerationPoll";
import { api, ApiError } from "@/lib/api";
import type { PostResponse } from "@/lib/types";
import { useState, useEffect } from "react";
import Link from "next/link";

export default function DashboardHome() {
  const { job, polling, start } = useGenerationPoll();
  const [latestPost, setLatestPost] = useState<PostResponse | null>(null);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState("");
  const [terminalLogs, setTerminalLogs] = useState<string[]>([
    "[SYSTEM] Connection established.",
    "[SYSTEM] Awaiting objective input..."
  ]);

  useEffect(() => {
    loadLatestPost();
  }, []);

  useEffect(() => {
    if (job) {
      const time = new Date().toLocaleTimeString();
      let logMsg = `[${time}] [JOB:${job.job_id.slice(0, 6)}] Status: ${job.status.toUpperCase()}`;
      if (job.progress_message) logMsg += ` - ${job.progress_message}`;
      setTerminalLogs(prev => [...prev, logMsg]);

      if (job.status === "done") {
        if (job.post_id) {
          api.getPost(job.post_id)
            .then(p => setLatestPost(p))
            .catch(() => loadLatestPost());
        } else {
          loadLatestPost();
        }
      }
    }
  }, [job]);

  async function loadLatestPost() {
    try {
      const drafts = await api.listPosts("draft");
      if (drafts && drafts.length > 0) {
        setLatestPost(drafts[0]);
      }
    } catch (e) {
      // Quiet fallback
    }
  }

  async function handleGenerate() {
    setError("");
    setTerminalLogs([`[${new Date().toLocaleTimeString()}] [SYSTEM] Triggering generation loop...`]);
    try {
      await start();
    } catch (e) {
      if (e instanceof ApiError) setError(e.message);
      else setError("Failed to start generation");
      setTerminalLogs(prev => [...prev, `[ERR] Generation trigger declined: ${e instanceof Error ? e.message : 'Unknown error'}`]);
    }
  }

  function handleCopy() {
    if (!latestPost) return;
    navigator.clipboard.writeText(latestPost.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <div className="max-w-4xl mx-auto p-8 space-y-6">
      {/* Header Block with title and aligned generate button */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-text-primary">Welcome back</h1>
          <div className="text-sm font-mono mt-2 flex items-center gap-2">
            {job?.status === "done" || latestPost ? (
              <>
                <span className="h-2 w-2 rounded-full bg-success" />
                <span className="text-text-muted font-medium">[ACTIVE] Post draft ready</span>
              </>
            ) : (
              <>
                <span className="h-2 w-2 rounded-full bg-accent" />
                <span className="text-text-muted font-medium">[READY] Standing by for input.</span>
              </>
            )}
          </div>
        </div>

        <div>
          <button
            onClick={handleGenerate}
            disabled={polling}
            className="rounded-[4px] bg-gradient-to-r from-[#ea580c] to-[#fbbf24] hover:from-[#d97706] hover:to-[#f59e0b] px-4 py-2 text-sm font-semibold text-background shadow-md transition-all duration-300 disabled:opacity-40"
          >
            {polling ? `[${job?.status?.toUpperCase() || 'GENERATING'}...]` : "Generate today's post"}
          </button>
        </div>
      </div>

      {/* Dynamic Terminal Status Output */}
      {polling && (
        <div className="border border-borderMuted bg-[#09090B] p-4 rounded-container font-mono text-xs text-textMuted space-y-1">
          {terminalLogs.map((log, idx) => (
            <div key={idx} className={log.includes("ERR") ? "text-danger" : log.includes("DONE") ? "text-success" : ""}>
              {log}
            </div>
          ))}
        </div>
      )}

      {/* Render Dynamic Latest Generated Post */}
      {latestPost && (
        <div className="border border-borderMuted bg-surface rounded-container overflow-hidden max-w-3xl">
          <div className="flex justify-between items-center bg-[#18181B] px-4 py-3 border-b border-borderMuted">
            <span className="text-xs font-mono font-medium px-2 py-0.5 rounded bg-[#27272A] text-[#FAFAFA] tracking-wide uppercase">
              {latestPost.content_pillar || "LINKEDIN"}
            </span>
            {latestPost.quality_score !== null && (
              <span className="text-xs font-mono font-medium text-textMuted">
                QUALITY SCORE <span className="text-[#FAFAFA] font-bold">{latestPost.quality_score}</span>/100
              </span>
            )}
          </div>
          <div className="p-4 space-y-4 bg-surface">
            <p className="text-sm text-textPrimary/95 leading-relaxed font-sans whitespace-pre-wrap">
              {latestPost.content}
            </p>
            <div className="flex justify-between items-center pt-2">
              <button
                onClick={handleCopy}
                className="text-xs text-textMuted hover:text-accent font-mono"
              >
                {copied ? "[Copied to Clipboard!]" : "[Copy to Clipboard]"}
              </button>
              <Link href="/dashboard/posts" className="text-xs text-accent hover:underline font-mono">
                [View & edit all drafts →]
              </Link>
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="text-xs text-danger font-mono border border-danger/25 bg-danger/5 p-2 rounded-interactive">
          [ERR] {error}
        </div>
      )}
    </div>
  );
}

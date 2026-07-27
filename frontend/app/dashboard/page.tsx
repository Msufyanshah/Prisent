"use client";
import { useGenerationPoll } from "@/hooks/useGenerationPoll";
import { ApiError } from "@/lib/api";
import { useState, useEffect } from "react";
import Link from "next/link";

const STATUS_LABELS: Record<string, string> = {
  pending: "Starting...",
  researching: "Researching...",
  writing: "Writing...",
  reviewing: "Reviewing...",
  done: "Done",
  failed: "Failed"
};

export default function DashboardHome() {
  const { job, polling, start } = useGenerationPoll();
  const [error, setError] = useState("");
  const [terminalLogs, setTerminalLogs] = useState<string[]>([
    "[SYSTEM] Connection established.",
    "[SYSTEM] Awaiting objective input..."
  ]);

  useEffect(() => {
    if (job) {
      const time = new Date().toLocaleTimeString();
      let logMsg = `[${time}] [JOB:${job.job_id.slice(0, 6)}] Status: ${job.status.toUpperCase()}`;
      if (job.progress_message) logMsg += ` - ${job.progress_message}`;
      setTerminalLogs(prev => [...prev, logMsg]);
    }
  }, [job]);

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

  return (
    <div className="max-w-4xl mx-auto p-8 space-y-6">
      {/* Header Block with title and aligned generate button */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-text-primary">Welcome back, Alex</h1>
          <div className="text-sm font-mono mt-2 flex items-center gap-2">
            {job?.status === "done" ? (
              <>
                <span className="h-2 w-2 rounded-full bg-success" />
                <span className="text-text-muted font-medium">[SUCCESS] Post generated</span>
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
            className="rounded-[4px] bg-accent px-4 py-2 text-sm font-medium text-background hover:bg-accent-hover transition-colors disabled:opacity-40"
          >
            {polling ? "Generating today's post..." : "Generate today's post"}
          </button>
        </div>
      </div>

      {job?.status === "done" && (
        <div className="border border-border-muted bg-surface rounded-container overflow-hidden max-w-3xl">
          <div className="flex justify-between items-center bg-[#18181B] px-4 py-3 border-b border-border-muted">
            <span className="text-xs font-mono font-medium px-2 py-0.5 rounded bg-[#27272A] text-[#FAFAFA] tracking-wide">LINKEDIN</span>
            <span className="text-xs font-mono font-medium text-text-muted">QUALITY SCORE <span className="text-[#FAFAFA] font-bold">94</span></span>
          </div>
          <div className="p-4 space-y-4 bg-surface">
            <p className="text-sm text-text-primary/95 leading-relaxed font-sans">
              The future of B2B SaaS isn't just about adding AI features. It's about fundamentally restructuring execution layers to be AI-native from day one. When your infrastructure is built for autonomous agent interaction, the velocity of deployment shifts from weeks to minutes. Here's a technical breakdown of how we engineered the new execution
            </p>
            <div className="flex justify-between items-center pt-2">
              <button
                onClick={() => navigator.clipboard.writeText("The future of B2B SaaS isn't just about adding AI features...")}
                className="text-xs text-text-muted hover:text-accent font-mono"
              >
                [Copy to Clipboard]
              </button>
              <Link href="/dashboard/posts" className="text-xs text-accent hover:underline font-mono">
                [View all drafts →]
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

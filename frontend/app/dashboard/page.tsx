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
    <div className="flex h-screen overflow-hidden">
      {/* Left panel - Main Workspace Canvas */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        <div>
          <h1 className="text-2xl font-medium tracking-tight">Welcome back, Alex</h1>
          <p className="text-sm text-textMuted font-mono">
            {job?.status === "done" ? "• [SUCCESS] Post generated" : "• [READY] Standing by for input."}
          </p>
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

        {job?.status === "done" && (
          <div className="border border-borderMuted bg-surface rounded-container overflow-hidden">
            <div className="flex justify-between items-center bg-[#1F1F23]/45 px-4 py-3 border-b border-borderMuted">
              <span className="text-xs font-mono font-medium tracking-wider text-textMuted uppercase">LINKEDIN</span>
              <span className="text-xs font-mono font-semibold text-accent uppercase">QUALITY SCORE 94</span>
            </div>
            <div className="p-4 space-y-4">
              <p className="text-sm text-textPrimary/95 leading-relaxed font-sans">
                The future of B2B SaaS isn't just about adding AI features. It's about fundamentally restructuring execution layers to be AI-native from day one. When your infrastructure is built for autonomous agent interaction, the velocity of deployment shifts from weeks to minutes. Here's a technical breakdown of how we engineered the new execution
              </p>
              <div className="flex justify-between items-center pt-2">
                <button
                  onClick={() => navigator.clipboard.writeText("The future of B2B SaaS isn't just about adding AI features...")}
                  className="text-xs text-textMuted hover:text-accent font-mono"
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

      {/* Right panel - Fixed 380px Live Telemetry Terminal */}
      <div className="w-[380px] shrink-0 border-l border-borderMuted bg-[#09090B] flex flex-col h-full">
        <div className="p-4 border-b border-borderMuted bg-surface flex justify-between items-center">
          <span className="text-xs font-mono font-medium tracking-wider text-textMuted uppercase">SYSTEM TELEMETRY LOGS</span>
          <span className={`h-2 w-2 rounded-full ${polling ? "bg-accent animate-pulse" : "bg-success"}`} />
        </div>
        <div className="flex-1 overflow-y-auto p-4 font-mono text-xs text-textPrimary/80 space-y-2 selection:bg-accent/30">
          {terminalLogs.map((log, index) => (
            <div key={index} className="leading-relaxed break-all">
              {log}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

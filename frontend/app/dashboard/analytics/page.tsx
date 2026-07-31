"use client";
import React, { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { AnalyticsSummary, PostAnalytics } from "@/lib/types";
import { Sparkles } from "lucide-react";

export default function AnalyticsPage() {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [posts, setPosts] = useState<PostAnalytics[]>([]);
  const [insight, setInsight] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [summaryData, postsData, insightData] = await Promise.all([
          api.getAnalyticsSummary(),
          api.getAnalyticsPosts(),
          api.getAnalyticsInsight(),
        ]);
        setSummary(summaryData);
        setPosts(postsData);
        setInsight(insightData.insight);
      } catch (err: any) {
        console.error("Failed to load analytics:", err);
        setError(err.message || "An error occurred while loading analytics data");
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  function formatNumber(num: number): string {
    if (num >= 1000) {
      return `${(num / 1000).toFixed(1)}k`;
    }
    return num.toString();
  }

  function getDayLabel(dateStr: string | null): string {
    if (!dateStr) return "";
    const date = new Date(dateStr);
    return date.toLocaleDateString(undefined, { weekday: "short" });
  }

  if (loading) {
    return (
      <div className="p-6 flex flex-col items-center justify-center min-h-[400px] space-y-4">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-accent border-t-transparent" />
        <span className="text-sm font-mono text-textMuted animate-pulse">Analyzing published metrics...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6 space-y-4 max-w-4xl">
        <h1 className="text-2xl font-medium tracking-tight text-red-500">Analytics Error</h1>
        <p className="text-sm text-textMuted">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="px-4 py-2 bg-accent text-[#09090B] font-mono text-xs uppercase tracking-wider rounded font-bold hover:bg-amber-500 transition-colors"
        >
          Retry Load
        </button>
      </div>
    );
  }

  // Map posts to chart coordinates (last 7 posts, oldest to newest)
  const chartPosts = [...posts].reverse().slice(-7);
  const maxMetric = Math.max(...chartPosts.map(p => p.reactions + p.comments), 10);
  
  const points = chartPosts.map((p, idx) => {
    const x = 10 + (idx / (chartPosts.length - 1 || 1)) * 580;
    const metric = p.reactions + p.comments;
    const y = 190 - (metric / maxMetric) * 160;
    return { x, y, post: p };
  });

  const pathD = points.length > 1
    ? `M ${points.map(p => `${p.x} ${p.y}`).join(" L ")}`
    : points.length === 1
      ? `M 10 110 L 590 110` // horizontal line in center
      : "M 10 200 L 590 200"; // horizontal line at bottom

  const fillD = points.length > 1
    ? `${pathD} L ${points[points.length - 1].x} 200 L ${points[0].x} 200 Z`
    : points.length === 1
      ? "M 10 110 L 590 110 L 590 200 L 10 200 Z"
      : "M 10 200 L 590 200 Z";

  const yLabels = [
    formatNumber(Math.round(maxMetric)),
    formatNumber(Math.round(maxMetric * 0.75)),
    formatNumber(Math.round(maxMetric * 0.5)),
    formatNumber(Math.round(maxMetric * 0.25)),
    "0"
  ];

  return (
    <div className="p-6 space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-medium tracking-tight">Analytics</h1>
        <p className="text-sm text-textMuted">Overview of published content performance metrics.</p>
      </div>

      {/* Numerical Metrics Cards (4-up) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        <div className="border border-borderMuted bg-surface p-4 rounded-container space-y-1">
          <span className="text-xs font-mono font-medium text-textMuted uppercase">Total posts</span>
          <div className="text-2xl font-mono font-bold tracking-tight">{summary?.total_posts_published ?? 0}</div>
        </div>
        <div className="border border-borderMuted bg-surface p-4 rounded-container space-y-1">
          <span className="text-xs font-mono font-medium text-textMuted uppercase">Avg impressions</span>
          <div className="text-2xl font-mono font-bold tracking-tight">
            {summary?.avg_impressions !== undefined ? formatNumber(summary.avg_impressions) : "0"}
          </div>
        </div>
        <div className="border border-borderMuted bg-surface p-4 rounded-container space-y-1">
          <span className="text-xs font-mono font-medium text-textMuted uppercase">Avg reactions</span>
          <div className="text-2xl font-mono font-bold tracking-tight">
            {summary?.avg_reactions !== undefined ? formatNumber(summary.avg_reactions) : "0"}
          </div>
        </div>
        <div className="border border-borderMuted bg-surface p-4 rounded-container space-y-1">
          <span className="text-xs font-mono font-medium text-textMuted uppercase">Best pillar</span>
          <div className="text-2xl font-mono font-bold tracking-tight text-[#D97706] truncate">
            {summary?.best_pillar ?? "N/A"}
          </div>
        </div>
      </div>

      {/* Chart Section */}
      <div className="border border-borderMuted bg-surface p-6 rounded-container space-y-4">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-sm font-medium uppercase tracking-wider text-textMuted">Engagement over time</h2>
          </div>
          <div className="flex items-center space-x-2">
            <span className="h-2 w-2 rounded-full bg-[#D97706]" />
            <span className="text-xs font-mono text-textMuted">Reactions + Comments</span>
          </div>
        </div>

        {/* Custom SVG Line Chart */}
        <div className="w-full h-64 bg-[#09090B]/50 border border-borderMuted/30 rounded-container p-4 flex flex-col justify-between">
          <div className="flex-grow flex">
            {/* Y Axis Labels */}
            <div className="flex flex-col justify-between text-[10px] font-mono text-textMuted pr-3 select-none text-right w-10 h-[calc(100%-8px)]">
              {yLabels.map((lbl, idx) => (
                <span key={idx}>{lbl}</span>
              ))}
            </div>

            {/* SVG Chart Area */}
            <div className="flex-1 relative h-[calc(100%-8px)]">
              <svg className="w-full h-full" viewBox="0 0 600 200" preserveAspectRatio="none">
                {/* Grid Lines */}
                <line x1="0" y1="0" x2="600" y2="0" stroke="#27272A" strokeDasharray="4 4" strokeWidth="0.5" />
                <line x1="0" y1="50" x2="600" y2="50" stroke="#27272A" strokeDasharray="4 4" strokeWidth="0.5" />
                <line x1="0" y1="100" x2="600" y2="100" stroke="#27272A" strokeDasharray="4 4" strokeWidth="0.5" />
                <line x1="0" y1="150" x2="600" y2="150" stroke="#27272A" strokeDasharray="4 4" strokeWidth="0.5" />
                <line x1="0" y1="200" x2="600" y2="200" stroke="#27272A" strokeWidth="0.5" />

                {/* Smooth curve line */}
                <path
                  d={pathD}
                  fill="none"
                  stroke="url(#strokeGradient)"
                  strokeWidth="3"
                  strokeLinecap="round"
                />

                {/* Chart Area Fill Gradient */}
                <path
                  d={fillD}
                  fill="url(#chartGradient)"
                  opacity="0.1"
                />

                <defs>
                  <linearGradient id="strokeGradient" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stopColor="#ea580c" />
                    <stop offset="100%" stopColor="#fbbf24" />
                  </linearGradient>
                  <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#ea580c" />
                    <stop offset="100%" stopColor="#fbbf24" stopOpacity="0" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
          </div>

          {/* X Axis Labels */}
          <div className="flex justify-between items-center text-[10px] font-mono text-textMuted pl-[52px] pr-2 pt-2">
            {points.length > 0 ? (
              points.map((p, idx) => (
                <span key={idx}>{getDayLabel(p.post.published_at)}</span>
              ))
            ) : (
              ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((day) => (
                <span key={day}>{day}</span>
              ))
            )}
          </div>
        </div>
      </div>

      {/* AI Insight & Top Posts Row */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Top 5 Posts Table */}
        <div className="md:col-span-2 border border-borderMuted bg-surface p-6 rounded-container space-y-4">
          <h2 className="text-sm font-medium uppercase tracking-wider text-textMuted">Top performing posts</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-sm">
              <thead>
                <tr className="border-b border-borderMuted/30 text-xs uppercase font-mono text-textMuted">
                  <th className="py-2 pr-4 font-normal">Preview</th>
                  <th className="py-2 px-4 font-normal text-right">Reactions</th>
                  <th className="py-2 pl-4 font-normal text-right">Comments</th>
                </tr>
              </thead>
              <tbody>
                {posts.slice(0, 5).map((post) => (
                  <tr key={post.post_id} className="border-b border-borderMuted/30 hover:bg-[#09090B]/20 transition-colors">
                    <td className="py-3 pr-4 text-textPrimary max-w-[200px] sm:max-w-[300px] truncate font-mono text-xs">{post.content_preview}...</td>
                    <td className="py-3 px-4 text-textPrimary text-right font-mono font-bold">{formatNumber(post.reactions)}</td>
                    <td className="py-3 pl-4 text-textPrimary text-right font-mono font-bold">{formatNumber(post.comments)}</td>
                  </tr>
                ))}
                {posts.length === 0 && (
                  <tr>
                    <td colSpan={3} className="py-8 text-center text-textMuted font-mono text-xs">
                      No published posts found. Post some content to see analytics!
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* AI Insight Card */}
        <div className="border border-borderMuted bg-surface p-6 rounded-container flex flex-col justify-between space-y-4">
          <div className="space-y-3">
            <div className="flex items-center space-x-2 text-[#D97706]">
              <Sparkles size={18} />
              <h2 className="text-sm font-medium uppercase tracking-wider font-mono">AI Growth Insight</h2>
            </div>
            <p className="text-xs text-textMuted leading-relaxed font-sans">
              {insight || "Once you publish content, your AI assistant will analyze performance trends to suggest optimizations."}
            </p>
          </div>
          <div className="pt-2 border-t border-borderMuted/30 text-[10px] font-mono text-textMuted">
            Powered by GPT-4o-mini
          </div>
        </div>
      </div>
    </div>
  );
}

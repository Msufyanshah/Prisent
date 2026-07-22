"use client";
import React from "react";

export default function AnalyticsPage() {
  return (
    <div className="p-6 space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-medium tracking-tight">Analytics</h1>
        <p className="text-sm text-textMuted">Overview of published content performance metrics.</p>
      </div>

      {/* Numerical Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="border border-borderMuted bg-surface p-4 rounded-container space-y-1">
          <span className="text-xs font-mono font-medium text-textMuted uppercase">Total posts published</span>
          <div className="text-2xl font-mono font-bold tracking-tight">1,248</div>
        </div>
        <div className="border border-borderMuted bg-surface p-4 rounded-container space-y-1">
          <span className="text-xs font-mono font-medium text-textMuted uppercase">Average impressions</span>
          <div className="text-2xl font-mono font-bold tracking-tight">45.2K</div>
        </div>
        <div className="border border-borderMuted bg-surface p-4 rounded-container space-y-1">
          <span className="text-xs font-mono font-medium text-textMuted uppercase">Average reactions</span>
          <div className="text-2xl font-mono font-bold tracking-tight">3,892</div>
        </div>
      </div>

      {/* Chart Section */}
      <div className="border border-borderMuted bg-surface p-6 rounded-container space-y-4">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-sm font-medium uppercase tracking-wider text-textMuted">Performance over time</h2>
          </div>
          <div className="flex items-center space-x-2">
            <span className="h-2 w-2 rounded-full bg-accent" />
            <span className="text-xs font-mono text-textMuted">Impressions</span>
          </div>
        </div>

        {/* Custom SVG Line Chart */}
        <div className="w-full h-64 relative bg-[#09090B]/50 border border-borderMuted/30 rounded-container overflow-hidden p-4">
          <svg className="w-full h-full" viewBox="0 0 600 200" preserveAspectRatio="none">
            {/* Grid Lines */}
            <line x1="0" y1="50" x2="600" y2="50" stroke="#27272A" strokeDasharray="4 4" strokeWidth="0.5" />
            <line x1="0" y1="100" x2="600" y2="100" stroke="#27272A" strokeDasharray="4 4" strokeWidth="0.5" />
            <line x1="0" y1="150" x2="600" y2="150" stroke="#27272A" strokeDasharray="4 4" strokeWidth="0.5" />

            {/* Smooth curve line (matching Stitch's mockup) */}
            <path
              d="M 10 150 C 100 130, 150 110, 200 90 C 250 70, 300 80, 350 95 C 400 110, 450 100, 500 40 C 530 5, 570 15, 590 35"
              fill="none"
              stroke="#D97706"
              strokeWidth="3.5"
              strokeLinecap="round"
            />

            {/* Chart Area Fill Gradient */}
            <path
              d="M 10 150 C 100 130, 150 110, 200 90 C 250 70, 300 80, 350 95 C 400 110, 450 100, 500 40 C 530 5, 570 15, 590 35 L 590 200 L 10 200 Z"
              fill="url(#chartGradient)"
              opacity="0.1"
            />

            <defs>
              <linearGradient id="chartGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#D97706" />
                <stop offset="100%" stopColor="#D97706" stopOpacity="0" />
              </linearGradient>
            </defs>
          </svg>

          {/* X Axis Labels */}
          <div className="flex justify-between items-center text-[10px] font-mono text-textMuted pt-2">
            <span>Mon</span>
            <span>Tue</span>
            <span>Wed</span>
            <span>Thu</span>
            <span>Fri</span>
            <span>Sat</span>
            <span>Sun</span>
          </div>
        </div>
      </div>
    </div>
  );
}

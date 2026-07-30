"use client";
import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";
import type { PostResponse } from "@/lib/types";

const FILTERS = ["draft", "scheduled", "published"];

export default function PostsPage() {
  const [posts, setPosts] = useState<PostResponse[]>([
    {
      id: "1",
      content: "The future of B2B SaaS isn't just about adding AI features. It's about fundamental workflow restructuring. We're seeing a shift where execution speed outpaces raw analytical capability in determining market leaders...",
      hook: null,
      topic: null,
      content_pillar: "Thought leadership",
      quality_score: 94,
      status: "draft",
      scheduled_at: null,
      published_at: null,
      linkedin_post_id: null,
      impressions: 0,
      reactions: 0,
      comments: 0
    },
    {
      id: "2",
      content: "Implementing vector databases at scale requires more than just standard indexing. Our engineering team recently overhauled our semantic search infrastructure, reducing latency by 40% while handling 10x the data volume...",
      hook: null,
      topic: null,
      content_pillar: "Technical deep dive",
      quality_score: 88,
      status: "draft",
      scheduled_at: null,
      published_at: null,
      linkedin_post_id: null,
      impressions: 0,
      reactions: 0,
      comments: 0
    },
    {
      id: "3",
      content: "We're excited to announce our upcoming feature set focused entirely on autonomous background agent loops. This release introduces deterministic schema checking and isolated runtime sandboxes for every agent worker thread.",
      hook: null,
      topic: null,
      content_pillar: "Company update",
      quality_score: null,
      status: "draft",
      scheduled_at: null,
      published_at: null,
      linkedin_post_id: null,
      impressions: 0,
      reactions: 0,
      comments: 0
    }
  ]);
  const [filter, setFilter] = useState("draft");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [activePost, setActivePost] = useState<PostResponse | null>(null);

  useEffect(() => {
    loadPosts();
  }, [filter]);

  async function loadPosts() {
    setLoading(true);
    try {
      const result = await api.listPosts(filter);
      if (result && result.length > 0) {
        setPosts(result);
      }
    } catch (e) {
      if (e instanceof ApiError) setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleAction(action: string, post: PostResponse) {
    try {
      if (action === "approve") {
        const scheduledAt = new Date(Date.now() + 3600_000).toISOString();
        await api.approvePost(post.id, scheduledAt);
      } else if (action === "publish-now") {
        await api.publishNow(post.id);
      }
      await loadPosts();
    } catch (e) {
      if (e instanceof ApiError) setError(e.message);
    }
  }

  return (
    <div className="flex h-screen overflow-hidden bg-background">
      {/* Left Column: Posts List */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6">
        {/* Navigation Tabs */}
        <div className="flex border-b border-borderMuted space-x-6">
          {FILTERS.map(f => {
            const active = filter === f;
            return (
              <button
                key={f}
                onClick={() => setFilter(f)}
                className={`pb-2 text-sm font-medium uppercase tracking-wider border-b-2 transition-colors -mb-[2px] ${
                  active
                    ? "border-accent text-accent"
                    : "border-transparent text-textMuted hover:text-textPrimary"
                }`}
              >
                {f}
              </button>
            );
          })}
        </div>

        {error && (
          <div className="text-xs text-danger font-mono border border-danger/25 bg-danger/5 p-2 rounded-interactive">
            [ERR] {error}
          </div>
        )}

        {loading ? (
          <div className="text-center py-12 text-sm text-textMuted font-mono">LOADING DATA RECORDS...</div>
        ) : (
          <div className="space-y-4">
            {posts
              .filter(p => p.status === filter)
              .map(post => {
                const isSelected = activePost?.id === post.id;
                return (
                  <div
                    key={post.id}
                    onClick={() => setActivePost(post)}
                    className={`border p-4 rounded-container transition-all cursor-pointer ${
                      isSelected
                        ? "border-accent bg-surface"
                        : "border-borderMuted bg-surface/45 hover:bg-surface/75"
                    }`}
                  >
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-mono text-xs text-textMuted uppercase">
                        {post.content_pillar || "General"}
                      </span>
                      {post.quality_score !== null && (
                        <span className="font-mono text-xs font-semibold text-accent">
                          Score: {post.quality_score}/100
                        </span>
                      )}
                    </div>
                    <p className="text-sm text-textPrimary/90 leading-relaxed font-sans mb-4">
                      {post.content}
                    </p>

                    <div className="flex justify-between items-center" onClick={e => e.stopPropagation()}>
                      <div className="text-xs text-textMuted font-mono">
                        {post.status === "published" && post.linkedin_post_id && (
                          <span>
                            {post.impressions} Views · {post.reactions} Likes · {post.comments} Comments
                          </span>
                        )}
                      </div>
                      <div className="flex space-x-2">
                        {post.status === "draft" && (
                          <button
                            onClick={() => handleAction("approve", post)}
                            className="px-3 py-1.5 rounded-interactive bg-accent text-xs font-medium text-background hover:bg-accent-hover transition-colors"
                          >
                            Approve & Schedule
                          </button>
                        )}
                        {post.status === "scheduled" && (
                          <button
                            onClick={() => handleAction("publish-now", post)}
                            className="px-3 py-1.5 rounded-interactive border border-borderMuted text-xs font-medium hover:bg-borderMuted/30 transition-colors"
                          >
                            Publish Now
                          </button>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
          </div>
        )}
      </div>

      {/* Right Column: Active Post Detail Panel */}
      {activePost && (
        <div className="w-[380px] shrink-0 border-l border-borderMuted bg-surface flex flex-col h-full">
          <div className="p-4 border-b border-borderMuted flex justify-between items-center bg-[#1F1F23]/45">
            <span className="text-xs font-mono font-medium text-textMuted">POST EDITOR</span>
            <button
              onClick={() => setActivePost(null)}
              className="text-xs text-textMuted hover:text-textPrimary font-mono"
            >
              [CLOSE]
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            <div>
              <label className="block text-xs font-medium text-textMuted uppercase mb-1">Content Block</label>
              <textarea
                value={activePost.content}
                onChange={e => {
                  const updated = { ...activePost, content: e.target.value };
                  setActivePost(updated);
                  setPosts(posts.map(p => (p.id === activePost.id ? updated : p)));
                }}
                className="w-full h-80 rounded-interactive border border-borderMuted bg-background p-3 text-sm text-textPrimary leading-relaxed focus:border-accent focus:outline-none"
              />
            </div>
            <div className="border-t border-borderMuted pt-4 space-y-2">
              <div className="text-xs text-textMuted font-mono">
                [PILLAR] {activePost.content_pillar?.toUpperCase() || "NOT SPECIFIED"}
              </div>
              <div className="text-xs text-textMuted font-mono">
                [STATUS] {activePost.status.toUpperCase()}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

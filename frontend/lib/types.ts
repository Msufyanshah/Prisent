export interface PersonaResponse {
  id: string;
  user_id: string;
  name: string;
  headline: string;
  niche: string;
  content_pillars: string[];
  tone: "professional" | "conversational" | "bold" | "storytelling";
  target_audience: string;
  content_goal: "grow_followers" | "get_clients" | "build_authority" | "network";
  posting_frequency: "daily" | "3x_week" | "2x_week" | "weekly";
  avoid_topics: string[];
  unique_differentiator: string;
}

export interface PostResponse {
  id: string;
  content: string;
  hook: string | null;
  topic: string | null;
  content_pillar: string | null;
  quality_score: number | null;
  status: "draft" | "scheduled" | "published" | "failed";
  scheduled_at: string | null;
  published_at: string | null;
  linkedin_post_id: string | null;
  impressions: number;
  reactions: number;
  comments: number;
}

export interface GenerationJob {
  job_id: string;
  status: "pending" | "researching" | "writing" | "reviewing" | "done" | "failed";
  progress_message: string;
  post_id: string | null;
  error: string | null;
}

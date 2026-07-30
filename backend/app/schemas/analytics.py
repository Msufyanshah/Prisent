from pydantic import BaseModel
from typing import Optional

class AnalyticsSummary(BaseModel):
    total_posts_published: int
    avg_impressions: float
    avg_reactions: float
    avg_comments: float
    best_pillar: Optional[str]

class PostAnalytics(BaseModel):
    post_id: str
    content_preview: str
    pillar: Optional[str]
    impressions: int
    reactions: int
    comments: int
    published_at: Optional[str]

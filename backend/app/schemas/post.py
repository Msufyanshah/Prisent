# backend/app/schemas/post.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class ApprovePostRequest(BaseModel):
    scheduled_at: datetime

class PostResponse(BaseModel):
    id: UUID
    user_id: UUID
    agent_job_id: Optional[UUID]
    content: str
    hook: Optional[str]
    topic: Optional[str]
    content_pillar: Optional[str]
    quality_score: Optional[int]
    status: str
    scheduled_at: Optional[datetime]
    published_at: Optional[datetime]
    linkedin_post_id: Optional[str]
    impressions: int
    reactions: int
    comments: int
    reposts: int
    failure_reason: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

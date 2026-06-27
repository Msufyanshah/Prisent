import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base, get_utc_now

class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    agent_job_id = Column(UUID(as_uuid=True), ForeignKey("agent_jobs.id"), nullable=True)
    content = Column(Text, nullable=False)
    hook = Column(String(500), nullable=True)                      # first line
    topic = Column(String(255), nullable=True)
    content_pillar = Column(String(255), nullable=True)
    quality_score = Column(Integer, nullable=True)                 # 0-100
    status = Column(String(20), nullable=False, default="draft")   # draft|scheduled|published|failed
    scheduled_at = Column(DateTime, nullable=True)
    published_at = Column(DateTime, nullable=True)
    linkedin_post_id = Column(String(255), nullable=True)
    impressions = Column(Integer, default=0)
    reactions = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    reposts = Column(Integer, default=0)
    failure_reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=get_utc_now, nullable=False)
    updated_at = Column(DateTime, default=get_utc_now, onupdate=get_utc_now)

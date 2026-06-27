import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.database import Base

class AgentJob(Base):
    __tablename__ = "agent_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="pending")
    # pending|researching|writing|reviewing|done|failed
    progress_message = Column(String(255), nullable=True)
    research_output = Column(JSONB, nullable=True)
    draft_content = Column(Text, nullable=True)
    review_notes = Column(Text, nullable=True)
    quality_score = Column(Integer, nullable=True)
    retries = Column(Integer, default=0)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

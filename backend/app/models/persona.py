import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from app.database import Base

class Persona(Base):
    __tablename__ = "personas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    headline = Column(String(255), nullable=False)
    niche = Column(String(255), nullable=False)
    content_pillars = Column(ARRAY(String), nullable=False)       # max 3
    tone = Column(String(50), nullable=False)                      # professional|conversational|bold|storytelling
    target_audience = Column(Text, nullable=False)
    content_goal = Column(String(50), nullable=False)              # grow_followers|get_clients|build_authority|network
    posting_frequency = Column(String(20), nullable=False)         # daily|3x_week|2x_week|weekly
    avoid_topics = Column(ARRAY(String), nullable=True, default=[])
    unique_differentiator = Column(Text, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

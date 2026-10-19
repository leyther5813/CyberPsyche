import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from app.core.database import Base

class ResilienceProfile(Base):
    __tablename__ = "resilience_profile"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("session.id", ondelete="CASCADE"), nullable=False, index=True)
    phase = Column(String, nullable=False)  # baseline | retest | transfer
    metrics_json = Column(JSON, nullable=False)  # Dictionary of calculated resilience constructs

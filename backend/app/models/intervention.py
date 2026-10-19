import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from app.core.database import Base

class Intervention(Base):
    __tablename__ = "intervention"

    id = Column(String, primary_key=True)  # e.g., "INT-AUTH-01"
    type = Column(String, nullable=False)  # targeted | generic
    lesson_code = Column(String, nullable=False, index=True)  # e.g., LESSON_AUTH_VULNERABILITY
    content_version = Column(String, nullable=False, default="v1.0")

class InterventionDelivery(Base):
    __tablename__ = "intervention_delivery"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("session.id", ondelete="CASCADE"), nullable=False, unique=True)
    intervention_id = Column(String, ForeignKey("intervention.id", ondelete="SET NULL"), nullable=True)
    intervention_type = Column(String, nullable=False)  # targeted | generic
    lesson_code = Column(String, nullable=False)  # e.g., LESSON_AUTH_VULNERABILITY
    practice_score = Column(Integer, nullable=True)  # Micro-exercise score
    completed_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

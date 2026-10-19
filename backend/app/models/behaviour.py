import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class BehaviourEvent(Base):
    __tablename__ = "behaviour_event"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("session.id", ondelete="CASCADE"), nullable=False, index=True)
    scenario_id = Column(String, ForeignKey("scenario.id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String, nullable=False)  # view | open_evidence | action | reason | confidence
    payload = Column(JSON, nullable=True)
    ts = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    session = relationship("Session", back_populates="events")

class Decision(Base):
    __tablename__ = "decision"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("session.id", ondelete="CASCADE"), nullable=False, index=True)
    scenario_id = Column(String, ForeignKey("scenario.id", ondelete="CASCADE"), nullable=False, index=True)
    action = Column(String, nullable=False)  # PROCEED | IGNORE | REPLY_TO_SENDER | VERIFY_INDEPENDENTLY | REPORT | ASK_TRUSTED_PERSON | GATHER_MORE_EVIDENCE | UNSURE
    reason_tags = Column(JSON, nullable=False)  # List of selected reason strings
    free_text = Column(Text, nullable=True)
    confidence = Column(Integer, nullable=False)  # 1-5 scale
    latency_ms = Column(Integer, nullable=False)
    submitted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    session = relationship("Session", back_populates="decisions")
    outcome = relationship("ScenarioOutcome", back_populates="decision", uselist=False, cascade="all, delete-orphan")

class ScenarioOutcome(Base):
    __tablename__ = "scenario_outcome"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    decision_id = Column(String, ForeignKey("decision.id", ondelete="CASCADE"), nullable=False, unique=True)
    decision_quality = Column(Float, nullable=False)  # 1.0 | 0.5 | 0.0
    under_caution = Column(Boolean, nullable=False, default=False)
    over_caution = Column(Boolean, nullable=False, default=False)
    verified = Column(Boolean, nullable=False, default=False)
    evidence_depth = Column(Float, nullable=False)  # 0.0 to 1.0
    reason_alignment_flag = Column(Boolean, nullable=False, default=True)

    decision = relationship("Decision", back_populates="outcome")

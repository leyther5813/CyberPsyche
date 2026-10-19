import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Session(Base):
    __tablename__ = "session"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True)
    arm = Column(String, nullable=False)  # targeted | generic
    form_assignment = Column(String, nullable=False)  # Form_A | Form_B
    current_phase = Column(String, nullable=False, default="baseline")  # consent | onboarding | baseline | intervention | retest | transfer | profile
    started_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    scenario_set_version = Column(String, nullable=False, default="scenario_set_v1")

    user = relationship("User", back_populates="sessions")
    session_scenarios = relationship("SessionScenario", back_populates="session", cascade="all, delete-orphan")
    events = relationship("BehaviourEvent", back_populates="session", cascade="all, delete-orphan")
    decisions = relationship("Decision", back_populates="session", cascade="all, delete-orphan")

class SessionScenario(Base):
    __tablename__ = "session_scenario"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("session.id", ondelete="CASCADE"), nullable=False, index=True)
    scenario_id = Column(String, ForeignKey("scenario.id", ondelete="CASCADE"), nullable=False, index=True)
    phase = Column(String, nullable=False)  # baseline | retest | transfer
    order_idx = Column(Integer, nullable=False)

    session = relationship("Session", back_populates="session_scenarios")

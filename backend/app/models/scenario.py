import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Scenario(Base):
    __tablename__ = "scenario"

    id = Column(String, primary_key=True)  # e.g., "EDU-AUTH-URG-MAL-01"
    family_id = Column(String, nullable=False, index=True)
    phase_pool = Column(String, nullable=False, index=True)  # baseline | retest | transfer | delayed
    context = Column(String, nullable=False)  # education_career | finance | social_messaging
    channel = Column(String, nullable=False)  # email | chat
    persona = Column(String, nullable=True)
    truth = Column(String, nullable=False)  # malicious | genuine | ambiguous
    mechanisms = Column(JSON, nullable=False)  # ["authority", "urgency"]
    pressure = Column(String, nullable=False)  # low | medium | high
    difficulty = Column(String, nullable=False)  # low | medium | high
    json_payload = Column(JSON, nullable=False)  # Complete frozen scenario JSON
    version = Column(String, nullable=False, default="scenario_set_v1")

    evidence_items = relationship("EvidenceItem", back_populates="scenario", cascade="all, delete-orphan")

class EvidenceItem(Base):
    __tablename__ = "evidence_item"

    id = Column(String, primary_key=True)  # e.g., "EDU-AUTH-URG-MAL-01-e1"
    scenario_id = Column(String, ForeignKey("scenario.id", ondelete="CASCADE"), nullable=False, index=True)
    label = Column(String, nullable=False)
    value = Column(String, nullable=False)
    signal = Column(String, nullable=False)  # suspicious | neutral | trustworthy | hidden
    diagnosticity = Column(String, nullable=False)  # high | medium | low
    official_channel = Column(Boolean, default=False, nullable=False)

    scenario = relationship("Scenario", back_populates="evidence_items")

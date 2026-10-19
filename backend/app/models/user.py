import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email_hash = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="participant", nullable=False)  # participant | researcher | admin
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    consents = relationship("Consent", back_populates="user", cascade="all, delete-orphan")
    digital_context = relationship("DigitalContext", back_populates="user", uselist=False, cascade="all, delete-orphan")
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")

class Consent(Base):
    __tablename__ = "consent"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    version = Column(String, nullable=False, default="1.0")
    accepted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", back_populates="consents")

class DigitalContext(Base):
    __tablename__ = "digital_context"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, unique=True)
    life_stage = Column(String, nullable=True)
    activities = Column(JSON, nullable=True)  # List of activity strings
    cyber_level = Column(String, nullable=True)  # Self-rated experience level 1-5
    interests = Column(JSON, nullable=True)

    user = relationship("User", back_populates="digital_context")

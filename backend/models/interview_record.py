from sqlalchemy import Column, String, DateTime, Float, JSON, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from core.database import Base


class InterviewRecord(Base):
    __tablename__ = "interview_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    candidate_name = Column(String(255), nullable=False)
    role_name = Column(String(255), nullable=False)
    role_description = Column(String, nullable=True)
    declared_seniority = Column(String(50), nullable=True)
    ai_detected_seniority = Column(String(50), nullable=True)
    final_score = Column(Float, nullable=False, default=0.0)
    technical_score = Column(Float, nullable=False, default=0.0)
    behavioral_score = Column(Float, nullable=False, default=0.0)
    duration_seconds = Column(Integer, nullable=True)
    skills = Column(JSON, nullable=True)
    technical_questions = Column(JSON, nullable=True)
    behavioral_questions = Column(JSON, nullable=True)
    final_report = Column(JSON, nullable=True)
    fit_analysis = Column(JSON, nullable=True)
    weighted_score = Column(JSON, nullable=True)
    language = Column(String(2), nullable=False, default="es")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User")
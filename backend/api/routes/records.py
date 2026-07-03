from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List
from datetime import datetime
from core.database import get_db
from core.auth import get_current_user, require_not_viewer
from models.user import User
from models.interview_record import InterviewRecord

router = APIRouter(prefix="/api/v1/records", tags=["records"])


class RecordCreateInput(BaseModel):
    candidate_name: str
    role_name: str
    role_description: Optional[str] = None
    declared_seniority: Optional[str] = None
    ai_detected_seniority: Optional[str] = None
    final_score: float = 0.0
    technical_score: float = 0.0
    behavioral_score: float = 0.0
    duration_seconds: Optional[int] = None
    skills: Optional[list] = None
    technical_questions: Optional[list] = None
    behavioral_questions: Optional[list] = None
    final_report: Optional[dict] = None
    fit_analysis: Optional[dict] = None
    weighted_score: Optional[dict] = None
    language: str = "es"


class RecordOut(BaseModel):
    id: str
    user_id: str
    user_name: str
    candidate_name: str
    role_name: str
    role_description: Optional[str]
    declared_seniority: Optional[str]
    ai_detected_seniority: Optional[str]
    final_score: float
    technical_score: float
    behavioral_score: float
    duration_seconds: Optional[int]
    skills: Optional[list]
    technical_questions: Optional[list]
    behavioral_questions: Optional[list]
    final_report: Optional[dict]
    fit_analysis: Optional[dict]
    weighted_score: Optional[dict]
    language: str
    created_at: datetime
    updated_at: datetime


def _to_out(r: InterviewRecord, user_name: str) -> RecordOut:
    return RecordOut(
        id=str(r.id),
        user_id=str(r.user_id),
        user_name=user_name,
        candidate_name=r.candidate_name,
        role_name=r.role_name,
        role_description=r.role_description,
        declared_seniority=r.declared_seniority,
        ai_detected_seniority=r.ai_detected_seniority,
        final_score=r.final_score,
        technical_score=r.technical_score,
        behavioral_score=r.behavioral_score,
        duration_seconds=r.duration_seconds,
        skills=r.skills,
        technical_questions=r.technical_questions,
        behavioral_questions=r.behavioral_questions,
        final_report=r.final_report,
        fit_analysis=r.fit_analysis,
        weighted_score=r.weighted_score,
        language=r.language,
        created_at=r.created_at,
        updated_at=r.updated_at,
    )


@router.post("", response_model=RecordOut)
def create_record(
    payload: RecordCreateInput,
    current_user: User = Depends(require_not_viewer),
    db: Session = Depends(get_db),
):
    record = InterviewRecord(
        user_id=current_user.id,
        candidate_name=payload.candidate_name,
        role_name=payload.role_name,
        role_description=payload.role_description,
        declared_seniority=payload.declared_seniority,
        ai_detected_seniority=payload.ai_detected_seniority,
        final_score=payload.final_score,
        technical_score=payload.technical_score,
        behavioral_score=payload.behavioral_score,
        duration_seconds=payload.duration_seconds,
        skills=payload.skills,
        technical_questions=payload.technical_questions,
        behavioral_questions=payload.behavioral_questions,
        final_report=payload.final_report,
        fit_analysis=payload.fit_analysis,
        weighted_score=payload.weighted_score,
        language=payload.language,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return _to_out(record, current_user.full_name)


@router.get("", response_model=List[RecordOut])
def list_records(
    only_mine: bool = Query(False, description="Si es true, solo entrevistas del usuario actual"),
    search: Optional[str] = Query(None, description="Buscar por nombre de candidato o rol"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(InterviewRecord)

    if only_mine:
        q = q.filter(InterviewRecord.user_id == current_user.id)

    if search:
        like = f"%{search}%"
        q = q.filter(
            (InterviewRecord.candidate_name.ilike(like))
            | (InterviewRecord.role_name.ilike(like))
        )

    q = q.order_by(desc(InterviewRecord.created_at))
    records = q.offset(skip).limit(limit).all()

    users_map = {u.id: u.full_name for u in db.query(User).all()}
    return [_to_out(r, users_map.get(r.user_id, "Desconocido")) for r in records]


@router.get("/{record_id}", response_model=RecordOut)
def get_record(
    record_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = db.query(InterviewRecord).filter(InterviewRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Entrevista no encontrada")
    user = db.query(User).filter(User.id == record.user_id).first()
    user_name = user.full_name if user else "Desconocido"
    return _to_out(record, user_name)


@router.delete("/{record_id}")
def delete_record(
    record_id: str,
    current_user: User = Depends(require_not_viewer),
    db: Session = Depends(get_db),
):
    record = db.query(InterviewRecord).filter(InterviewRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Entrevista no encontrada")

    if record.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=403,
            detail="Solo el creador o un admin puede eliminar esta entrevista",
        )

    db.delete(record)
    db.commit()
    return {"ok": True, "deleted_id": record_id}
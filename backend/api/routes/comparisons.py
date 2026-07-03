from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List
from datetime import datetime
from core.database import get_db
from core.auth import get_current_user, require_not_viewer
from models.user import User
from models.comparison import Comparison

router = APIRouter(prefix="/api/v1/comparisons", tags=["comparisons"])


class ComparisonCreateInput(BaseModel):
    title: str
    role_name: str
    role_description: Optional[str] = None
    rounds: list = []
    language: str = "es"


class ComparisonUpdateInput(BaseModel):
    title: Optional[str] = None
    role_name: Optional[str] = None
    role_description: Optional[str] = None
    rounds: Optional[list] = None


class ComparisonOut(BaseModel):
    id: str
    user_id: str
    user_name: str
    title: str
    role_name: str
    role_description: Optional[str]
    rounds: list
    language: str
    created_at: datetime
    updated_at: datetime


def _to_out(c: Comparison, user_name: str) -> ComparisonOut:
    return ComparisonOut(
        id=str(c.id),
        user_id=str(c.user_id),
        user_name=user_name,
        title=c.title,
        role_name=c.role_name,
        role_description=c.role_description,
        rounds=c.rounds or [],
        language=c.language,
        created_at=c.created_at,
        updated_at=c.updated_at,
    )


@router.post("", response_model=ComparisonOut)
def create_comparison(
    payload: ComparisonCreateInput,
    current_user: User = Depends(require_not_viewer),
    db: Session = Depends(get_db),
):
    comp = Comparison(
        user_id=current_user.id,
        title=payload.title,
        role_name=payload.role_name,
        role_description=payload.role_description,
        rounds=payload.rounds,
        language=payload.language,
    )
    db.add(comp)
    db.commit()
    db.refresh(comp)
    return _to_out(comp, current_user.full_name)


@router.get("", response_model=List[ComparisonOut])
def list_comparisons(
    only_mine: bool = Query(False),
    search: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    q = db.query(Comparison)
    if only_mine:
        q = q.filter(Comparison.user_id == current_user.id)
    if search:
        like = f"%{search}%"
        q = q.filter(
            (Comparison.title.ilike(like)) | (Comparison.role_name.ilike(like))
        )
    q = q.order_by(desc(Comparison.created_at))
    comparisons = q.offset(skip).limit(limit).all()

    users_map = {u.id: u.full_name for u in db.query(User).all()}
    return [_to_out(c, users_map.get(c.user_id, "Desconocido")) for c in comparisons]


@router.get("/{comparison_id}", response_model=ComparisonOut)
def get_comparison(
    comparison_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    comp = db.query(Comparison).filter(Comparison.id == comparison_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Comparación no encontrada")
    user = db.query(User).filter(User.id == comp.user_id).first()
    user_name = user.full_name if user else "Desconocido"
    return _to_out(comp, user_name)


@router.put("/{comparison_id}", response_model=ComparisonOut)
def update_comparison(
    comparison_id: str,
    payload: ComparisonUpdateInput,
    current_user: User = Depends(require_not_viewer),
    db: Session = Depends(get_db),
):
    comp = db.query(Comparison).filter(Comparison.id == comparison_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Comparación no encontrada")

    if comp.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=403,
            detail="Solo el creador o un admin puede editar esta comparación",
        )

    if payload.title is not None:
        comp.title = payload.title
    if payload.role_name is not None:
        comp.role_name = payload.role_name
    if payload.role_description is not None:
        comp.role_description = payload.role_description
    if payload.rounds is not None:
        comp.rounds = payload.rounds

    db.commit()
    db.refresh(comp)
    user = db.query(User).filter(User.id == comp.user_id).first()
    return _to_out(comp, user.full_name if user else "Desconocido")


@router.delete("/{comparison_id}")
def delete_comparison(
    comparison_id: str,
    current_user: User = Depends(require_not_viewer),
    db: Session = Depends(get_db),
):
    comp = db.query(Comparison).filter(Comparison.id == comparison_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Comparación no encontrada")

    if comp.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=403,
            detail="Solo el creador o un admin puede eliminar esta comparación",
        )

    db.delete(comp)
    db.commit()
    return {"ok": True, "deleted_id": comparison_id}
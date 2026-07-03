from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from core.auth import get_current_user, require_admin, hash_password
from models.user import User, UserRole

router = APIRouter(prefix="/api/v1/users", tags=["users"])


class UserOut(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    is_active: bool


class UserCreateInput(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "recruiter"


class UserUpdateInput(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    role: str | None = None
    is_active: bool | None = None
    new_password: str | None = None


def _to_out(u: User) -> UserOut:
    return UserOut(
        id=str(u.id),
        email=u.email,
        full_name=u.full_name,
        role=u.role.value,
        is_active=u.is_active,
    )


@router.get("", response_model=List[UserOut])
def list_users(
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    users = db.query(User).order_by(User.created_at.asc()).all()
    return [_to_out(u) for u in users]


@router.post("", response_model=UserOut)
def create_user(
    payload: UserCreateInput,
    _: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya esta registrado",
        )

    try:
        role = UserRole(payload.role.lower())
    except ValueError:
        role = UserRole.RECRUITER

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name.strip(),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return _to_out(user)


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: str,
    payload: UserUpdateInput,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    is_self = str(user.id) == str(admin.id)

    if is_self:
        if payload.role is not None and payload.role.lower() != user.role.value:
            raise HTTPException(
                status_code=400,
                detail="No puedes cambiar tu propio rol",
            )
        if payload.is_active is not None and payload.is_active != user.is_active:
            raise HTTPException(
                status_code=400,
                detail="No puedes cambiar tu propio estado de activación",
            )

    if payload.email is not None and payload.email != user.email:
        existing = db.query(User).filter(User.email == payload.email).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Ya existe otro usuario con ese email",
            )
        user.email = payload.email

    if payload.full_name is not None:
        user.full_name = payload.full_name.strip()
    if not is_self and payload.role is not None:
        try:
            user.role = UserRole(payload.role.lower())
        except ValueError:
            pass
    if not is_self and payload.is_active is not None:
        user.is_active = payload.is_active
    if payload.new_password:
        user.password_hash = hash_password(payload.new_password)

    db.commit()
    db.refresh(user)
    return _to_out(user)


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    if str(user_id) == str(admin.id):
        raise HTTPException(status_code=400, detail="No puedes eliminarte a ti mismo")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(user)
    db.commit()
    return {"ok": True, "deleted_id": str(user_id)}
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from core.database import get_db
from core.auth import hash_password, verify_password, create_access_token, get_current_user
from models.user import User, UserRole
from fastapi import Request
from core.rate_limit import limiter

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


class RegisterInput(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "recruiter"


class LoginInput(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


@router.post("/register", response_model=UserOut)
@limiter.limit("3/hour")
def register(request: Request, payload: RegisterInput, db: Session = Depends(get_db)):
    is_first_user = db.query(User).count() == 0
    if not is_first_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El registro público está deshabilitado. Contacta a un admin.",
        )
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya esta registrado",
        )

    is_first_user = db.query(User).count() == 0

    try:
        role = UserRole(payload.role.lower())
    except ValueError:
        role = UserRole.RECRUITER

    if is_first_user:
        role = UserRole.ADMIN

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        full_name=payload.full_name.strip(),
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserOut(
        id=str(user.id),
        email=user.email,
        full_name=user.full_name,
        role=user.role.value,
        is_active=user.is_active,
    )


@router.post("/login", response_model=TokenOut)
@limiter.limit("5/minute")
def login(request: Request, payload: LoginInput, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado",
        )

    token = create_access_token({"sub": str(user.id)})
    return TokenOut(
        access_token=token,
        user=UserOut(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            role=user.role.value,
            is_active=user.is_active,
        ),
    )

@router.post("/login-form", response_model=TokenOut)
@limiter.limit("5/minute")
def login_form(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario desactivado",
        )

    token = create_access_token({"sub": str(user.id)})
    return TokenOut(
        access_token=token,
        user=UserOut(
            id=str(user.id),
            email=user.email,
            full_name=user.full_name,
            role=user.role.value,
            is_active=user.is_active,
        ),
    )

@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return UserOut(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role.value,
        is_active=current_user.is_active,
    )

from core.encryption import encrypt, decrypt


class ApiKeyInput(BaseModel):
    api_key: str


class ApiKeyStatus(BaseModel):
    has_api_key: bool
    api_key_preview: str


@router.post("/me/api-key")
def save_my_api_key(
    payload: ApiKeyInput,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    key = payload.api_key.strip()
    if not key:
        current_user.groq_api_key_encrypted = None
    else:
        current_user.groq_api_key_encrypted = encrypt(key)
    db.commit()
    return {"ok": True}


@router.get("/me/api-key", response_model=ApiKeyStatus)
def get_my_api_key_status(current_user: User = Depends(get_current_user)):
    if not current_user.groq_api_key_encrypted:
        return ApiKeyStatus(has_api_key=False, api_key_preview="")
    key = decrypt(current_user.groq_api_key_encrypted)
    preview = f"{key[:6]}...{key[-4:]}" if len(key) > 12 else "***"
    return ApiKeyStatus(has_api_key=True, api_key_preview=preview)


@router.delete("/me/api-key")
def delete_my_api_key(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    current_user.groq_api_key_encrypted = None
    db.commit()
    return {"ok": True}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from core.rate_limit import limiter
from api.routes.transcribe import router as transcribe_router
from api.routes.health import router as health_router
from api.routes.ocr import router as ocr_router
from api.routes.classify import router as classify_router
from api.routes.interview import router as interview_router
from api.routes.report import router as report_router
from api.routes.scoring import router as scoring_router
from utils.config import APP_NAME, DEBUG
from ai.model.predict import load_models
from api.routes.auth import router as auth_router
from api.routes.records import router as records_router
from api.routes.comparisons import router as comparisons_router
from api.routes.users import router as users_router

app = FastAPI(title=APP_NAME, debug=DEBUG, version="0.1.0")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.on_event("startup")
async def startup_event():
    load_models()
    print("AI models loaded")

import os
from dotenv import load_dotenv

load_dotenv()

_allowed_origins_raw = os.getenv("ALLOWED_ORIGINS", "*")
if _allowed_origins_raw.strip() == "*":
    _allowed_origins = ["*"]
    _allow_credentials = False
else:
    _allowed_origins = [o.strip() for o in _allowed_origins_raw.split(",") if o.strip()]
    _allow_credentials = True

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(f"CORS allowed origins: {_allowed_origins}")

from fastapi import Request
from services.groq_service import set_current_api_key

@app.middleware("http")
async def inject_api_key(request: Request, call_next):
    """Inyecta la API key del usuario logueado (o del header como fallback)."""
    api_key = ""

    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header[7:]
        try:
            from core.auth import decode_token
            from core.database import SessionLocal
            from models.user import User
            from core.encryption import decrypt

            payload = decode_token(token)
            user_id = payload.get("sub")
            if user_id:
                db = SessionLocal()
                try:
                    user = db.query(User).filter(User.id == user_id).first()
                    if user and user.groq_api_key_encrypted:
                        api_key = decrypt(user.groq_api_key_encrypted)
                finally:
                    db.close()
        except Exception:
            pass

    if not api_key:
        api_key = request.headers.get("X-Groq-Api-Key", "")

    set_current_api_key(api_key)
    response = await call_next(request)
    return response
app.include_router(health_router, prefix="/api/v1")
app.include_router(ocr_router, prefix="/api/v1")
app.include_router(classify_router, prefix="/api/v1")
app.include_router(interview_router, prefix="/api/v1")
app.include_router(report_router, prefix="/api/v1")
app.include_router(scoring_router, prefix="/api/v1")
app.include_router(transcribe_router, prefix="/api/v1")
app.include_router(auth_router)
app.include_router(records_router)
app.include_router(comparisons_router)
app.include_router(users_router)

@app.get("/")
def root():
    return {"message": f"Welcome to {APP_NAME} API"}
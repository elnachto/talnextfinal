from fastapi import APIRouter
from models.schemas import HealthResponse
from utils.config import APP_NAME

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok",
        app=APP_NAME,
        version="0.1.0"
    )
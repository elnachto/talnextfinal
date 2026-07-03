from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.groq_service import generate_interview_questions, regenerate_single_question

router = APIRouter()

class CandidateInput(BaseModel):
    area: str
    seniority: str
    ai_detected_seniority: str = ""
    role_name: str = ""
    role_description: str = ""
    mode: str = "general"
    total_questions: int = 8
    questions_per_skill: int = 3
    axis_questions: dict[str, int] = {}
    include_behavioral: bool = True
    skills: list[str]
    selected_skills_context: list[dict] = []
    selected_skills: list[str] = []
    experience_years: int
    fit_analysis: dict | None = None
    language: str = "es"

class RegenerateInput(BaseModel):
    role_name: str = ""
    seniority: str = "Mid"
    experience_years: int = 0
    skill: str = ""
    category: str = ""
    axis: str = "Technical"
    competency: str = ""
    previous_question: str = ""
    difficulty: str = "similar"
    language: str = "es"

class GenerateSingleQuestionInput(BaseModel):
    role_name: str = ""
    seniority: str = "Mid"
    skill: str = ""
    category: str = ""
    axis: str = "Technical"
    competency: str = ""
    custom_question: str = ""
    count: int = 1
    language: str = "es"  


@router.post("/generate-single-question")
def generate_single_question(payload: GenerateSingleQuestionInput):
    try:
        from services.groq_service import generate_questions_for_bank
        result = generate_questions_for_bank(payload.dict(), language=payload.language)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-interview")
def generate_interview(candidate: CandidateInput):
    print(f"BACKEND ROUTE LANG RECIBIDO: {candidate.language}")
    try:
        result = generate_interview_questions(candidate.dict(), language=candidate.language)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/regenerate-question")
def regenerate_question(payload: RegenerateInput):
    try:
        result = regenerate_single_question(payload.dict(), language=payload.language)  
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
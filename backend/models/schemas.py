from pydantic import BaseModel

class HealthResponse(BaseModel):
    status: str
    app: str
    version: str

class CandidateClassification(BaseModel):
    seniority: str
    area: str
    skills: list[str]
    skills_by_category: dict[str, list[str]]
    experience_years: int
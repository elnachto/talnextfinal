from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ai.model.predict import predict_candidate
from services.groq_service import detect_skills_from_cv

router = APIRouter()

class FitAnalysisInput(BaseModel):
    cv_text: str
    role_name: str
    declared_seniority: str = ""
    role_description: str = ""
class TextInput(BaseModel):
    text: str

class CompareCandidatesInput(BaseModel):
    role_name: str = ""
    role_description: str = ""
    candidates: list[dict] = []
    anchors: list[dict] = []


@router.post("/classify")
def classify_candidate(input: TextInput):
    if not input.text.strip():
        raise HTTPException(status_code=400, detail="Texto vacío")

    try:
        result = predict_candidate(input.text)
        try:
            from services.groq_service import extract_cv_metadata
            metadata = extract_cv_metadata(input.text)
            result['cv_metadata'] = metadata
        except Exception:
            result['cv_metadata'] = {"name": "", "email": "", "phone": "", "location": ""}
        # El mergge
        try:
            groq_result = detect_skills_from_cv(
                input.text,
                known_skills=result.get('skills', []),
            )
            print(f"GROQ SKILLS DETECT RESULT: {groq_result}")
            groq_skills_by_cat = groq_result.get('skills_by_category', {})
            print(f"SKILLS BY CATEGORY: {groq_skills_by_cat}")

            if groq_skills_by_cat:
                # Conversion de skills de ia a formato
                merged = dict(result.get('skills_by_category', {}))

                for category, skills_list in groq_skills_by_cat.items():
                    existing = merged.get(category, [])
                    existing_names = {s.get('name', '') if isinstance(s, dict) else s for s in existing}

                    for skill in skills_list:
                        if skill not in existing_names:
                            existing.append({
                                'id': f'{category}::{skill}',
                                'name': skill,
                                'category': category,
                                'source': 'ai_fallback',
                            })
                    merged[category] = existing

                result['skills_by_category'] = merged

                all_skills = set(result.get('skills', []))
                all_skills.update(groq_result.get('skills', []))
                result['skills'] = sorted(all_skills)

                from ai.model.predict import _primary_skills_by_category
                result['primary_skills_by_category'] = _primary_skills_by_category(
                    result['skills'],
                    result['main_area'],
                    result.get('area_scores', {}),
                )

        except Exception as e:
            print(f"ERROR en detect_skills_from_cv: {e}")
            import traceback
            traceback.print_exc()

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-fit")
def analyze_fit(input: FitAnalysisInput):
    if not input.cv_text.strip() or not input.role_name.strip():
        raise HTTPException(status_code=400, detail="CV y rol son requeridos")
    try:
        from services.groq_service import analyze_cv_role_fit
        return analyze_cv_role_fit(
            cv_text=input.cv_text,
            role_name=input.role_name,
            declared_seniority=input.declared_seniority,
            role_description=input.role_description,
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/compare-candidates")
def compare_candidates_endpoint(input: CompareCandidatesInput):
    if not input.candidates:
        raise HTTPException(
            status_code=400,
            detail="Se requiere al menos 1 candidato para comparar"
        )
    try:
        from services.groq_service import compare_candidates
        return compare_candidates(input.dict())
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/test-groq")
def test_groq_connection():
    """
    Hace un ping mínimo a Groq con la API key del usuario.
    Devuelve estado + rate limits actuales.
    """
    try:
        from services.groq_service import _get_client
        client = _get_client()
        
        # Ping chiquitito a Groq
        response = client.chat.completions.with_raw_response.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": "hi"}],
            max_tokens=1,
            temperature=0,
        )
        
        # Extraer headers de rate limit
        headers = dict(response.headers)
        
        return {
            "status": "ok",
            "model_tested": "llama-3.1-8b-instant",
            "rate_limits": {
                "requests_limit": headers.get("x-ratelimit-limit-requests"),
                "requests_remaining": headers.get("x-ratelimit-remaining-requests"),
                "requests_reset": headers.get("x-ratelimit-reset-requests"),
                "tokens_limit": headers.get("x-ratelimit-limit-tokens"),
                "tokens_remaining": headers.get("x-ratelimit-remaining-tokens"),
                "tokens_reset": headers.get("x-ratelimit-reset-tokens"),
            },
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"No se pudo conectar a Groq: {str(e)}"
        )
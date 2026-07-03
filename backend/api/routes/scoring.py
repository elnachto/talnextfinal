from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.scoring_engine import compute_final_score, get_effective_weights, load_matrices

router = APIRouter()


class ScoreRequest(BaseModel):
    role_name: str
    seniority: str
    axis_scores: dict[str, float]


@router.post("/compute-score")
def compute_score(request: ScoreRequest):
    try:
        return compute_final_score(
            role_name=request.role_name,
            seniority=request.seniority,
            axis_scores=request.axis_scores,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/matrices")
def list_matrices():
    """Lista todas las matrices cargadas (debug/inspección)."""
    return load_matrices()


@router.get("/weights")
def get_weights(role_name: str, seniority: str = "Mid"):
    """Devuelve los pesos efectivos para un rol+seniority + el profile detectado."""
    from services.scoring_engine import get_matrix_for_role
    matrix = get_matrix_for_role(role_name)
    return {
        "role_name": role_name,
        "seniority": seniority,
        "weights": get_effective_weights(role_name, seniority),
        "matrix_profile": matrix.get("profile", "Default"),
    }

@router.get("/matrices-summary")
def matrices_summary():
    """Lista simplificada de matrices para mostrar en UI."""
    matrices = load_matrices()
    return [
        {
            "profile": m.get("profile"),
            "weights": m.get("weights", {}),
            "applies_to": m.get("applies_to", []),
        }
        for m in matrices
    ]
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.groq_service import generate_enterprise_report
from services.scoring_engine import compute_final_score

router = APIRouter()


class ReportRequest(BaseModel):
    candidate: dict
    setup: dict = {}
    axis_scores: dict[str, float] = {}
    questions_detail: list[dict] = []
    technical_score: float = 0
    behavioral_score: float = 0
    overall_score: float = 0
    skipped_count: int = 0
    regenerated_count: int = 0
    post_notes: dict = {}
    custom_weights: dict[str, float] | None = None
    forced_matrix_profile: str | None = None
    language: str = "es"


@router.post("/generate-report")
def create_report(request: ReportRequest):
    try:
        role_name = request.setup.get('role_name', '') or request.candidate.get('area', '')
        declared_seniority = request.setup.get('declared_seniority', '') or request.candidate.get('seniority', 'Mid')

        if request.custom_weights:
            total = sum(request.custom_weights.values())
            normalized = {k: v / total for k, v in request.custom_weights.items()} if total > 0 else request.custom_weights
            breakdown = {}
            final = 0.0
            for axis, weight in normalized.items():
                score = request.axis_scores.get(axis, 0)
                contribution = score * weight
                final += contribution
                breakdown[axis] = {
                    "score": round(score, 2),
                    "weight": round(weight, 4),
                    "contribution": round(contribution, 3),
                }
            weighted = {
                "final_score": round(final, 2),
                "weights_used": normalized,
                "breakdown": breakdown,
                "matrix_profile": "Custom",
            }
        elif request.forced_matrix_profile:
            from services.scoring_engine import load_matrices, get_effective_weights
            matrices = load_matrices()
            forced = next((m for m in matrices if m.get("profile") == request.forced_matrix_profile), None)
            if forced:
                weights = dict(forced.get("weights", {}))
                modifiers = forced.get("seniority_modifiers", {}).get(declared_seniority, {})
                for k, v in modifiers.items():
                    weights[k] = v
                total = sum(weights.values())
                if total > 0:
                    weights = {k: round(v / total, 4) for k, v in weights.items()}
                breakdown = {}
                final = 0.0
                for axis, weight in weights.items():
                    score = request.axis_scores.get(axis, 0)
                    contribution = score * weight
                    final += contribution
                    breakdown[axis] = {
                        "score": round(score, 2),
                        "weight": round(weight, 4),
                        "contribution": round(contribution, 3),
                    }
                weighted = {
                    "final_score": round(final, 2),
                    "weights_used": weights,
                    "breakdown": breakdown,
                    "matrix_profile": forced.get("profile"),
                }
            else:
                weighted = compute_final_score(
                    role_name=role_name,
                    seniority=declared_seniority,
                    axis_scores=request.axis_scores,
                )
        else:
            weighted = compute_final_score(
                role_name=role_name,
                seniority=declared_seniority,
                axis_scores=request.axis_scores,
            )

        narrative = generate_enterprise_report(
            candidate=request.candidate,
            setup=request.setup,
            axis_scores=request.axis_scores,
            questions_detail=request.questions_detail,
            weighted_score=weighted,
            stats={
                'skipped': request.skipped_count,
                'regenerated': request.regenerated_count,
                'technical_score': request.technical_score,
                'behavioral_score': request.behavioral_score,
                'overall_score': request.overall_score,
            },
            post_notes=request.post_notes,
            language=request.language,
        )

        return {
            **narrative,
            'weighted_score': weighted,
            'axis_scores': request.axis_scores,
            'setup_used': request.setup,
            'post_notes': request.post_notes,
            'stats': {
                'skipped': request.skipped_count,
                'regenerated': request.regenerated_count,
                'technical_score': round(request.technical_score, 2),
                'behavioral_score': round(request.behavioral_score, 2),
            },
            'seniority_comparison': {
                'declared': declared_seniority,
                'ai_detected': request.setup.get('ai_detected_seniority', request.candidate.get('seniority', '')),
                'has_discrepancy': declared_seniority.lower() != request.setup.get('ai_detected_seniority', request.candidate.get('seniority', '')).lower(),
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
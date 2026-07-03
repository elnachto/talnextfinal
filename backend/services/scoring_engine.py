"""
Weight matrix scoring engine.
Loads JSON matrices and computes weighted final scores.
"""

import json
import os
from typing import Dict, List, Optional

MATRICES_DIR = os.path.join("config", "matrices")

_loaded_matrices: Optional[List[dict]] = None


def load_matrices() -> List[dict]:
    """Carga todas las matrices desde JSON. Cache en memoria."""
    global _loaded_matrices
    if _loaded_matrices is not None:
        return _loaded_matrices

    matrices = []
    if not os.path.isdir(MATRICES_DIR):
        return matrices

    for fname in os.listdir(MATRICES_DIR):
        if fname.endswith(".json"):
            with open(os.path.join(MATRICES_DIR, fname), "r", encoding="utf-8") as f:
                matrices.append(json.load(f))

    _loaded_matrices = matrices
    return matrices


def get_matrix_for_role(role_name: str) -> dict:
    """
    Busca la matriz cuyo applies_to contiene el rol.
    Si no encuentra, retorna la matriz default.
    """
    matrices = load_matrices()
    role_lower = role_name.lower().strip()

    for matrix in matrices:
        for applies in matrix.get("applies_to", []):
            if applies.lower() == role_lower:
                return matrix

    for matrix in matrices:
        for applies in matrix.get("applies_to", []):
            applies_lower = applies.lower()
            if applies_lower in role_lower or role_lower in applies_lower:
                return matrix

    for matrix in matrices:
        if matrix.get("profile") == "Default":
            return matrix

    return matrices[0] if matrices else {
        "profile": "Empty",
        "weights": {"technical": 1.0},
        "seniority_modifiers": {},
    }


def get_effective_weights(role_name: str, seniority: str) -> Dict[str, float]:
    """Retorna los pesos efectivos aplicando modificadores de seniority."""
    matrix = get_matrix_for_role(role_name)
    weights = dict(matrix.get("weights", {}))
    modifiers = matrix.get("seniority_modifiers", {}).get(seniority, {})

    for key, value in modifiers.items():
        weights[key] = value

    total = sum(weights.values())
    if total > 0:
        weights = {k: round(v / total, 4) for k, v in weights.items()}

    return weights


def compute_final_score(
    role_name: str,
    seniority: str,
    axis_scores: Dict[str, float],
) -> dict:
    """
    Calcula el score final ponderado.

    axis_scores: dict con scores por eje (1-5), ej:
        {"technical": 4.2, "communication": 3.8, "cultural_fit": 4.0, ...}
    
    Returns: {final_score, weights_used, breakdown, matrix_profile}
    """
    weights = get_effective_weights(role_name, seniority)
    matrix = get_matrix_for_role(role_name)

    final = 0.0
    breakdown = {}

    for axis, weight in weights.items():
        score = axis_scores.get(axis, 0)
        contribution = score * weight
        final += contribution
        breakdown[axis] = {
            "score": round(score, 2),
            "weight": round(weight, 4),
            "contribution": round(contribution, 3),
        }

    return {
        "final_score": round(final, 2),
        "weights_used": weights,
        "breakdown": breakdown,
        "matrix_profile": matrix.get("profile", "Default"),
    }
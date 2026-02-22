"""
final_scorer.py

Enterprise-grade ATS final scoring engine.
Combines all resume intelligence signals into a single ATS score.
"""

from typing import Dict


WEIGHTS = {
    "skills": 0.45,
    "experience": 0.25,
    "projects": 0.15,
    "ats_format": 0.10,
    "role": 0.05,
}


def calculate_final_ats_score(
    skill_score: int,
    experience_score: int,
    project_score: int,
    ats_format_score: int,
    role_score: int,
) -> Dict[str, object]:
    """
    Calculate final ATS score using weighted formula.
    """

    final_score = (
        WEIGHTS["skills"] * skill_score +
        WEIGHTS["experience"] * experience_score +
        WEIGHTS["projects"] * project_score +
        WEIGHTS["ats_format"] * ats_format_score +
        WEIGHTS["role"] * role_score
    )

    final_score = round(final_score)

    return {
    "ats_score": final_score,
    "breakdown": {
        "skill_score": skill_score,
        "experience_score": experience_score,
        "project_score": project_score,
        "ats_format_score": ats_format_score,
        "role_score": role_score,
    },
    "weights": WEIGHTS,
}


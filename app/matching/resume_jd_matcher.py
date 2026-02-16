"""
resume_full_matcher.py

Enterprise-level full resume vs JD match score.
Combines semantic similarity + skill + experience + projects + role.
"""

from typing import Dict

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


# Load once (important for performance)
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_resume_jd_similarity(resume_text: str, jd_text: str) -> dict:
    """
    Calculates full semantic similarity between resume and JD.
    Returns percentage score (0–100).
    """

    if not resume_text or not jd_text:
        return {
            "resume_match_score": 0,
            "similarity_score": 0.0
        }

    # Generate embeddings
    resume_embedding = model.encode([resume_text])
    jd_embedding = model.encode([jd_text])

    # Cosine similarity
    similarity = cosine_similarity(resume_embedding, jd_embedding)[0][0]

    # Convert to percentage
    similarity_percent = round(float(similarity) * 100)

    return {
        "resume_match_score": similarity_percent,
        "similarity_score": round(float(similarity), 4)
    }

def calculate_resume_match_score_full(
    semantic_score: int,
    skill_score: int,
    experience_score: int,
    project_score: int,
    role_score: int,
) -> Dict[str, int]:
    """
    Calculates full resume match score using multiple intelligence signals.
    """

    WEIGHTS = {
        "semantic": 0.40,
        "skills": 0.25,
        "experience": 0.15,
        "projects": 0.10,
        "role": 0.10,
    }

    final_score = (
        WEIGHTS["semantic"] * semantic_score +
        WEIGHTS["skills"] * skill_score +
        WEIGHTS["experience"] * experience_score +
        WEIGHTS["projects"] * project_score +
        WEIGHTS["role"] * role_score
    )

    return {
        "resume_match_score": round(final_score),
        "weights": WEIGHTS
    }
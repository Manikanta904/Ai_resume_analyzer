"""
multi_jd.py

Recruiter-side engine to compare one resume against multiple
job descriptions and rank best fit roles.
"""

from typing import List, Dict

from app.skills.skill_extractor import extract_skills
from app.analysis.experience_analyzer import calculate_experience_score
from app.analysis.project_analyzer import calculate_project_relevance_score
from app.analysis.ats_checker import calculate_ats_format_score
from app.role_intelligence.role_detector import (
    detect_role,
    calculate_role_relevance_score,
)
from app.analysis.final_scorer import calculate_final_ats_score


def compare_resume_with_multiple_jds(
    resume_text: str,
    jd_texts: List[Dict[str, str]],
) -> Dict[str, object]:
    """
    Compare one resume against multiple job descriptions.

    Args:
        resume_text (str): Parsed resume text
        jd_texts (List[Dict]): [{"name": str, "text": str}]

    Returns:
        Dict with ranked JD comparison results
    """

    resume_skills = extract_skills(resume_text)
    results = []

    for jd in jd_texts:
        jd_name = jd["name"]
        jd_text = jd["text"]

        jd_skills = extract_skills(jd_text)

        # -------- Skill Matching --------
        matched_skills = list(set(resume_skills) & set(jd_skills))
        skill_score = int(
            (len(matched_skills) / max(len(jd_skills), 1)) * 100
        )

        # -------- Experience --------
        experience_result = calculate_experience_score(
            resume_text, jd_text
        )

        # -------- Projects --------
        project_result = calculate_project_relevance_score(
            resume_text, jd_skills, resume_skills
        )

        # -------- ATS Format --------
        ats_format_result = calculate_ats_format_score(resume_text)

        # -------- Role Intelligence --------
        detected_role = detect_role(jd_skills)
        role_result = calculate_role_relevance_score(
            resume_skills, detected_role
        )

        # -------- Final ATS Score --------
        final_score = calculate_final_ats_score(
            skill_score=skill_score,
            experience_score=experience_result["experience_score"],
            project_score=project_result["project_score"],
            ats_format_score=ats_format_result["ats_format_score"],
            role_score=role_result["role_score"],
        )

        results.append({
            "jd_name": jd_name,
            "role": role_result["role"],
            "final_ats_score": final_score["final_ats_score"],
            "breakdown": final_score["breakdown"],
        })

    # Sort by best ATS score
    results.sort(key=lambda x: x["final_ats_score"], reverse=True)

    return {
        "comparisons": results,
        "best_fit": results[0] if results else None,
    }
"""
ranking_engine.py

Recruiter-side engine to rank multiple resumes
against a single job description.
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


def rank_resumes_against_jd(
    resumes: List[Dict[str, str]],
    jd_text: str,
) -> Dict[str, object]:
    """
    Rank multiple resumes against a single job description.

    resumes: [{ "name": str, "text": str }]
    """

    jd_skills = extract_skills(jd_text)
    detected_role = detect_role(jd_skills)

    ranked_results = []

    for resume in resumes:
        resume_name = resume["name"]
        resume_text = resume["text"]

        resume_skills = extract_skills(resume_text)

        # -------- Skill score --------
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

        # -------- Role relevance --------
        role_result = calculate_role_relevance_score(
            resume_skills, detected_role
        )

        # -------- Final ATS score --------
        final_score = calculate_final_ats_score(
            skill_score=skill_score,
            experience_score=experience_result["experience_score"],
            project_score=project_result["project_score"],
            ats_format_score=ats_format_result["ats_format_score"],
            role_score=role_result["role_score"],
        )

        ranked_results.append({
            "candidate": resume_name,
            "final_ats_score": final_score["final_ats_score"],
            "breakdown": final_score["breakdown"],
            "matched_skills": matched_skills,
            "missing_skills": list(set(jd_skills) - set(matched_skills)),
        })

    # Sort candidates by ATS score
    ranked_results.sort(
        key=lambda x: x["final_ats_score"],
        reverse=True
    )

    return {
        "job_role": detected_role,
        "total_candidates": len(ranked_results),
        "rankings": ranked_results,
        "top_candidates": ranked_results[:3],
    }
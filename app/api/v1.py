"""
v1.py

Frontend-facing product APIs (Version 1).
Acts as orchestration layer over internal ATS engines.
"""

import os
from fastapi import APIRouter, UploadFile, File

from app.parsing.resume_parser import parse_resume
from app.parsing.jd_parser import parse_jd
from app.skills.skill_extractor import extract_skills
from app.matching.semantic_matcher import semantic_match
from app.matching.jd_skill_classifier import classify_jd_skills
from app.matching.weighted_scorer import calculate_ats_score
from app.matching.explainability import explain_score

from app.analysis.experience_analyzer import calculate_experience_score
from app.analysis.project_analyzer import calculate_project_relevance_score
from app.analysis.ats_checker import calculate_ats_format_score
from app.analysis.final_scorer import calculate_final_ats_score

from app.role_intelligence.role_detector import (
    detect_role,
    calculate_role_relevance_score,
)

UPLOAD_DIR = "uploads"

router = APIRouter(prefix="/api/v1", tags=["Product APIs"])

@router.post("/analyze")
async def analyze_resume(
    resume_file: UploadFile = File(...),
    jd_file: UploadFile = File(...),
):
    resume_path = os.path.join(UPLOAD_DIR, resume_file.filename)
    jd_path = os.path.join(UPLOAD_DIR, jd_file.filename)

    with open(resume_path, "wb") as f:
        f.write(await resume_file.read())

    with open(jd_path, "wb") as f:
        f.write(await jd_file.read())

    resume_text = parse_resume(resume_path)
    jd_text = parse_jd(jd_path)

    # ---------------- Skill Analysis ----------------
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    rule_matches = set(resume_skills) & set(jd_skills)
    semantic_matches = set(
        semantic_match(resume_skills, jd_skills)["matched_skills"]
    )

    matched_skills = sorted(rule_matches | semantic_matches)
    missing_skills = sorted(set(jd_skills) - set(matched_skills))

    jd_classification = classify_jd_skills(jd_text, jd_skills)

    skill_score = calculate_ats_score(
        matched_skills,
        jd_classification["must_have"],
        jd_classification["good_to_have"],
    )

    skill_explanation = explain_score(
        matched_skills,
        jd_classification["must_have"],
        jd_classification["good_to_have"],
    )

    # ---------------- Experience ----------------
    experience_result = calculate_experience_score(resume_text, jd_text)

    # ---------------- Projects ----------------
    project_result = calculate_project_relevance_score(
        resume_text,
        jd_skills,
        resume_skills,
    )

    # ---------------- ATS Format ----------------
    ats_format_result = calculate_ats_format_score(resume_text)

    # ---------------- Role Intelligence ----------------
    detected_role = detect_role(jd_skills)
    role_result = calculate_role_relevance_score(
        resume_skills,
        detected_role,
    )

    # ---------------- Final ATS Score ----------------
    final_score = calculate_final_ats_score(
        skill_score=skill_score,
        experience_score=experience_result["experience_score"],
        project_score=project_result["project_score"],
        ats_format_score=ats_format_result["ats_format_score"],
        role_score=role_result["role_score"],
    )

    return {
        "final_ats": final_score,
        "skills": {
            "matched": matched_skills,
            "missing": missing_skills,
            "explanation": skill_explanation,
        },
        "experience": experience_result,
        "projects": project_result,
        "ats_format": ats_format_result,
        "role": role_result,
    }

@router.post("/analyze")
async def analyze_resume(
    resume_file: UploadFile = File(...),
    jd_file: UploadFile = File(...),
):
    resume_path = os.path.join(UPLOAD_DIR, resume_file.filename)
    jd_path = os.path.join(UPLOAD_DIR, jd_file.filename)

    with open(resume_path, "wb") as f:
        f.write(await resume_file.read())

    with open(jd_path, "wb") as f:
        f.write(await jd_file.read())

    resume_text = parse_resume(resume_path)
    jd_text = parse_jd(jd_path)

    # ---------------- Skill Analysis ----------------
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    rule_matches = set(resume_skills) & set(jd_skills)
    semantic_matches = set(
        semantic_match(resume_skills, jd_skills)["matched_skills"]
    )

    matched_skills = sorted(rule_matches | semantic_matches)
    missing_skills = sorted(set(jd_skills) - set(matched_skills))

    jd_classification = classify_jd_skills(jd_text, jd_skills)

    skill_score = calculate_ats_score(
        matched_skills,
        jd_classification["must_have"],
        jd_classification["good_to_have"],
    )

    skill_explanation = explain_score(
        matched_skills,
        jd_classification["must_have"],
        jd_classification["good_to_have"],
    )

    # ---------------- Experience ----------------
    experience_result = calculate_experience_score(resume_text, jd_text)

    # ---------------- Projects ----------------
    project_result = calculate_project_relevance_score(
        resume_text,
        jd_skills,
        resume_skills,
    )

    # ---------------- ATS Format ----------------
    ats_format_result = calculate_ats_format_score(resume_text)

    # ---------------- Role Intelligence ----------------
    detected_role = detect_role(jd_skills)
    role_result = calculate_role_relevance_score(
        resume_skills,
        detected_role,
    )

    # ---------------- Final ATS Score ----------------
    final_score = calculate_final_ats_score(
        skill_score=skill_score,
        experience_score=experience_result["experience_score"],
        project_score=project_result["project_score"],
        ats_format_score=ats_format_result["ats_format_score"],
        role_score=role_result["role_score"],
    )

    return {
        "final_ats": final_score,
        "skills": {
            "matched": matched_skills,
            "missing": missing_skills,
            "explanation": skill_explanation,
        },
        "experience": experience_result,
        "projects": project_result,
        "ats_format": ats_format_result,
        "role": role_result,
    }
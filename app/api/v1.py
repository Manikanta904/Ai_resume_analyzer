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

from app.versioning.resume_versions import (
    generate_resume_id,
    save_resume_version,
)

from typing import List
from fastapi import UploadFile, File

from app.recruiter.multi_jd import compare_resume_with_multiple_jds
from app.recruiter.ranking_engine import rank_resumes_against_jd
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

    # ---------------- Resume Versioning ----------------
    resume_id = generate_resume_id()
    saved_version = save_resume_version(
        resume_id=resume_id,
        ats_score=final_score["final_ats_score"],
        role=role_result["role"],
        matched_skills=matched_skills,
        missing_skills=missing_skills,
    )
    return {
        "resume_id": resume_id,
        "version": saved_version["version"],
        "final_ats": final_score,
        "skills": {...},
        "experience": experience_result,
        "projects": project_result,
        "ats_format": ats_format_result,
        "role": role_result,
    }


    from app.versioning.resume_versions import get_resume_versions

      
    @router.get("/resume/{resume_id}/versions")
    def get_versions(resume_id: str):
        """
        Fetch all ATS score versions for a resume.
        """
        return get_resume_versions(resume_id)


@router.post("/analyze-multi-jd")
async def analyze_multi_jd(
    resume_file: UploadFile = File(...),
    jd_files: List[UploadFile] = File(...),
):
    """
    Compare one resume against multiple job descriptions.
    """

    # Save resume
    resume_path = os.path.join(UPLOAD_DIR, resume_file.filename)
    with open(resume_path, "wb") as f:
        f.write(await resume_file.read())

    resume_text = parse_resume(resume_path)

    # Parse all JDs
    jd_texts = []
    for jd_file in jd_files:
        jd_path = os.path.join(UPLOAD_DIR, jd_file.filename)
        with open(jd_path, "wb") as f:
            f.write(await jd_file.read())

        jd_texts.append({
            "name": jd_file.filename,
            "text": parse_jd(jd_path),
        })

    return compare_resume_with_multiple_jds(
        resume_text=resume_text,
        jd_texts=jd_texts,
    )

@router.post("/recruiter/rank-resumes")
async def rank_resumes(
    jd_file: UploadFile = File(...),
    resume_files: List[UploadFile] = File(...),
):
    """
    Recruiter API to rank multiple resumes against one JD.
    """

    # Parse JD
    jd_path = os.path.join(UPLOAD_DIR, jd_file.filename)
    with open(jd_path, "wb") as f:
        f.write(await jd_file.read())

    jd_text = parse_jd(jd_path)

    # Parse resumes
    resumes = []
    for resume_file in resume_files:
        resume_path = os.path.join(UPLOAD_DIR, resume_file.filename)
        with open(resume_path, "wb") as f:
            f.write(await resume_file.read())

        resumes.append({
            "name": resume_file.filename,
            "text": parse_resume(resume_path),
        })

    return rank_resumes_against_jd(
        resumes=resumes,
        jd_text=jd_text,
    )
from fastapi import FastAPI, UploadFile, File, HTTPException, Body
import os
import shutil
from fastapi import UploadFile, File, Body
from app.parsing.resume_parser import parse_resume
from app.parsing.jd_parser import parse_jd
from app.skills.skill_extractor import extract_skills
from app.matching.semantic_matcher import semantic_match
from app.matching.jd_skill_classifier import classify_jd_skills
from app.matching.skill_matcher import match_skills
from app.matching.weighted_scorer import calculate_ats_score
from app.matching.explainability import explain_score

from typing import Optional
from app.analysis.experience_analyzer import calculate_experience_score
from app.analysis.project_analyzer import calculate_project_relevance_score
from app.analysis.ats_checker import calculate_ats_format_score


# ✅ ONE app only
app = FastAPI(title="AI Resume Analyzer Backend")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def health_check():
    return {"status": "Backend is running"}


# -----------------------------
# Upload Resume
# -----------------------------
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Unsupported resume format")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = parse_resume(file_path)

    return {
        "filename": file.filename,
        "extracted_text_preview": text[:1000]
    }


# -----------------------------
# Upload JD
# -----------------------------
@app.post("/upload-jd")
async def upload_jd(file: UploadFile = File(...)):
    if not file.filename.endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Unsupported JD format")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = parse_jd(file_path)

    return {
        "filename": file.filename,
        "extracted_text_preview": text[:1000]
    }


# -----------------------------
# Extract Skills (raw text)
# -----------------------------
@app.post("/extract-skills")
async def extract_skills_api(text: str = Body(..., media_type="text/plain")):
    skills = extract_skills(text)
    return {
        "extracted_skills": skills,
        "count": len(skills)
    }


# -----------------------------
# ✅ DAY 8 ANALYZE ENDPOINT
# -----------------------------
@app.post("/analyze")
async def analyze(
    resume_file: UploadFile = File(...),
    jd_file: UploadFile = File(...)
):
    # ---------- 1. Save files ----------
    resume_path = os.path.join(UPLOAD_DIR, resume_file.filename)
    jd_path = os.path.join(UPLOAD_DIR, jd_file.filename)

    with open(resume_path, "wb") as f:
        f.write(await resume_file.read())

    with open(jd_path, "wb") as f:
        f.write(await jd_file.read())

    # ---------- 2. Parse text ----------
    resume_text = parse_resume(resume_path)
    jd_text = parse_jd(jd_path)

    if not resume_text.strip():
        resume_skills = []
    else:
        resume_skills = extract_skills(resume_text)

    if not jd_text.strip():
        jd_skills = []
    else:
        jd_skills = extract_skills(jd_text)


    # ---------- 3. Extract skills ----------
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    #DAY 9: Edge case handling ----------
    # Edge case handling
    if not resume_skills and not jd_skills:
        return {
            "error": "No skills detected in resume and job description",
            "resume_skills": [],
            "jd_skills": [],
            "ats_score": 0,
            "score_explanation": [
                "Neither resume nor job description contains recognizable skills"
            ]
        }

    if not resume_skills:
        return {
            "error": "No skills detected in resume",
            "resume_skills": [],
            "jd_skills": jd_skills,
            "ats_score": 0,
            "score_explanation": [
                "Resume does not contain recognizable skills"
            ]
        }

    if not jd_skills:
        return {
            "error": "No skills detected in job description",
            "resume_skills": resume_skills,
            "jd_skills": [],
            "ats_score": 0,
            "score_explanation": [
                "Job description does not contain recognizable skills"
            ]
        }


    # ---------- 4. Rule-based matching ----------
    rule_matches = set(resume_skills) & set(jd_skills)

    # ---------- 5. Semantic matching ----------
    semantic_result = semantic_match(resume_skills, jd_skills)
    semantic_matches = set(semantic_result["matched_skills"])

    # ---------- 6. Merge results (DAY 8 CORE) ----------
    final_matched = sorted(rule_matches | semantic_matches)
    final_missing = sorted(set(jd_skills) - set(final_matched))

    # ---------- 7. Classify JD skills ----------
    jd_classification = classify_jd_skills(jd_text, jd_skills)

    # ---------- 8. Weighted ATS score ----------
    ats_score = calculate_ats_score(
        final_matched,
        jd_classification["must_have"],
        jd_classification["good_to_have"]
    )

    # ---------- 9. Explainability ----------
    score_explanation = explain_score(
        final_matched,
        jd_classification["must_have"],
        jd_classification["good_to_have"]
    )

    if ats_score == 0:
        score_explanation.append("No must-have skills matched")

    return {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": final_matched,
        "missing_skills": final_missing,
        "must_have_skills": jd_classification["must_have"],
        "good_to_have_skills": jd_classification["good_to_have"],
        "ats_score": ats_score,
        "score_explanation": score_explanation,

        "_debug": {
            "rule_matches_count": len(rule_matches),
            "semantic_matches_count": len(semantic_matches)
        }
    }
# -----------------------------
# Experience Analysis API
# -----------------------------
@app.post("/analyze-experience")
async def analyze_experience(
    resume_file: UploadFile = File(...),
    jd_file: UploadFile = File(...)
):
    resume_path = os.path.join(UPLOAD_DIR, resume_file.filename)
    jd_path = os.path.join(UPLOAD_DIR, jd_file.filename)

    with open(resume_path, "wb") as f:
        f.write(await resume_file.read())

    with open(jd_path, "wb") as f:
        f.write(await jd_file.read())

    resume_text = parse_resume(resume_path)
    jd_text = parse_jd(jd_path)

    experience_result = calculate_experience_score(resume_text, jd_text)

    return {
        "experience_analysis": experience_result
    }


# -----------------------------
# Project Relevance Analysis API
# -----------------------------
@app.post("/analyze-projects")
async def analyze_projects(
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

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    project_result = calculate_project_relevance_score(
        resume_text=resume_text,
        jd_skills=jd_skills,
        known_skills=resume_skills,
    )

    return {
        "project_analysis": project_result
    }

# -----------------------------
# ATS Format Compatibility API
# -----------------------------
@app.post("/analyze-ats-format")
async def analyze_ats_format(resume_file: UploadFile = File(...)):
    resume_path = os.path.join(UPLOAD_DIR, resume_file.filename)

    with open(resume_path, "wb") as f:
        f.write(await resume_file.read())

    resume_text = parse_resume(resume_path)

    ats_result = calculate_ats_format_score(resume_text)

    return {
        "ats_format_analysis": ats_result
    }

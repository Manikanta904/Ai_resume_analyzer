from fastapi import FastAPI, UploadFile, File, HTTPException, Body,Form
import os
import shutil
from app.parsing.resume_parser import parse_resume
from app.parsing.jd_parser import parse_jd
from app.utils.text_validator import validate_min_words
from app.skills.skill_extractor import extract_skills
from app.matching.semantic_matcher import semantic_match
from app.matching.jd_skill_classifier import classify_jd_skills
from app.matching.skill_matcher import match_skills
from app.matching.weighted_scorer import calculate_ats_score
from app.matching.explainability import explain_score

from typing import Optional
from app.analysis.experience_analyzer import calculate_experience_score
from app.analysis.experience_analyzer import extract_experience_years

from app.analysis.project_analyzer import calculate_project_relevance_score
from app.analysis.ats_checker import calculate_ats_format_score
from app.recommendations.engine import generate_skill_gap_recommendations
from app.analysis.final_scorer import calculate_final_ats_score
from app.analysis.project_analyzer import analyze_projects_core
from app.analysis.ats_checker import calculate_ats_format_score
from app.role_intelligence.role_detector import detect_role, calculate_role_relevance_score
from app.ai_engine.ai_guard import ai_safe_execute
from app.analysis.fraud_detector import detect_resume_fraud

from app.role_intelligence.role_detector import (
    detect_role,
    calculate_role_relevance_score,
)

from app.ai_engine.skill_fallback import (
    detect_unknown_skills,
    classify_unknown_skills,
)

from app.analysis.section_analyzer import generate_section_feedback
from app.ai_engine.section_feedback_ai import generate_section_feedback_ai
from app.ai_engine.resume_rewrite_ai import rewrite_resume_for_jd
from app.recommendations.engine import generate_skill_gap_recommendations


from app.api.v1 import router as v1_router



# ✅ ONE app only
app = FastAPI(title="AI Resume Analyzer Backend")
app.include_router(v1_router)
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
#  ANALYZE ENDPOINT
# -----------------------------

@app.post("/analyze")
async def analyze(
    resume_file: Optional[UploadFile] = File(None),
    jd_file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None),
    jd_text: Optional[str] = Form(None),
):
    
# ---------------------------
# Resume input handling
# ---------------------------
    if resume_file and resume_file.filename:
        resume_path = os.path.join(UPLOAD_DIR, resume_file.filename)
        with open(resume_path, "wb") as f:
            f.write(await resume_file.read())
        resume_text = parse_resume(resume_path)

    elif resume_text and resume_text.strip() and resume_text != "string":
        resume_text = resume_text.strip()

    else:
        resume_text = ""

# ---------------------------
# JD input handling
# ---------------------------
    if jd_file and jd_file.filename:
        jd_path = os.path.join(UPLOAD_DIR, jd_file.filename)
        with open(jd_path, "wb") as f:
            f.write(await jd_file.read())
        jd_text = parse_jd(jd_path)

    elif jd_text and jd_text.strip() and jd_text != "string":
        jd_text = jd_text.strip()

    else:
        jd_text = ""

    if not resume_text or not jd_text:
        raise HTTPException(
            status_code=400,
            detail="Resume or Job Description content could not be extracted"
        )

    resume_valid = validate_min_words(resume_text)
    jd_valid = validate_min_words(jd_text)

    if not resume_valid and not jd_valid:
        raise HTTPException(
            status_code=400,
            detail="Resume and Job Description must each contain at least 20 words"
        )

    if not resume_valid:
        raise HTTPException(
            status_code=400,
            detail="Resume must contain at least 20 words"
        )

    if not jd_valid:
        raise HTTPException(
            status_code=400,
            detail="Job Description must contain at least 20 words"
        )


    


    # ---------- 3. Extract skills ----------
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

        # ---------- AI Fallback Skill Detection ----------
    unknown_resume_skills = detect_unknown_skills(resume_skills, jd_skills)
    ai_classified_skills = classify_unknown_skills(unknown_resume_skills)

    # Merge AI-detected skills
    # ai_classified_skills is a LIST of dicts
    # -------- Merge AI-detected skills (SAFE) --------
    for item in ai_classified_skills:
        # Case 1: dict
        if isinstance(item, dict):
            skill_name = item.get("skill")

        # Case 2: string
        elif isinstance(item, str):
            skill_name = item

        else:
            continue

        if skill_name and skill_name not in resume_skills:
            resume_skills.append(skill_name)


    # ---------- END AI Fallback Skill Detection ----------
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

    #---skill gap recommendations---    
    skill_gap_recommendations = generate_skill_gap_recommendations(final_missing)

    # ---------------------------
    # Skill Score (JD Coverage)
    # ---------------------------
    if jd_skills:
        skill_score = round((len(final_matched) / len(jd_skills)) * 100)
    else:
        skill_score = 0

    

    #---------experience score------------
    experience_result = calculate_experience_score(resume_text, jd_text)
    experience_score = experience_result.get("experience_score", 0)

    #---------project relevance score------------------------------

    project_result = analyze_projects_core(
        resume_text=resume_text,
        resume_skills=resume_skills,
        jd_skills=jd_skills,
)
    project_score = project_result["project_score"]


    #---------ATS format score----------------
    ats_format_result = calculate_ats_format_score(resume_text)
    ats_format_score = ats_format_result["ats_format_score"]

    #---------role relevance score----------------
        # Detect role from JD
    detected_role = detect_role(jd_skills)

    # Calculate role relevance score
    role_result = calculate_role_relevance_score(
        resume_skills=resume_skills,
        detected_role=detected_role
    )

    role_score = role_result["role_score"]



    # ---------- 7. Classify JD skills ----------
    jd_classification = classify_jd_skills(jd_text, jd_skills)

    # ---------- Resume Match Score (JD Coverage) ----------
    if jd_skills:
        resume_match_score = round(
            (len(final_matched) / len(jd_skills)) * 100
        )
    else:
        resume_match_score = 0

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

    # ---------- Edge case: zero ATS score ----------
    if ats_score == 0:
        score_explanation.append("No must-have skills matched")

    # ----------  Section Analysis ----------
    section_feedback= generate_section_feedback(
    resume_text=resume_text,
    jd_skills=jd_skills,
)
    # -----------------------------
    # SECTION-WISE FEEDBACK (AI)
    # -----------------------------

    section_feedback = ai_safe_execute(
        ai_function=generate_section_feedback_ai,
        fallback_function=generate_section_feedback,
        resume_text=resume_text,
        jd_text=jd_text
    )

    #--fraud detection--
    years_of_experience = extract_experience_years(resume_text)
    fraud_report = detect_resume_fraud(resume_skills, years_of_experience)

    final_ats = calculate_final_ats_score(
        skill_score=skill_score,
        experience_score=experience_score,
        project_score=project_score,
        ats_format_score=ats_format_score,
        role_score=role_score,
    )

    print("USING FINAL ATS:", final_ats)



    return {
        "resume_match_score": resume_match_score,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": final_matched,
        "missing_skills": final_missing,

        "skill_gap_recommendations": skill_gap_recommendations,
         "section_feedback": {
        "rule_based": section_feedback,
        "ai_based": section_feedback
    },
        "must_have_skills": jd_classification["must_have"],
        "good_to_have_skills": jd_classification["good_to_have"],
        "ats_score" : final_ats["ats_score"] ,
        "score_explanation": score_explanation,

        "fraud_report": fraud_report,



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
async def analyze_projects_api(
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


    # -----------------------------
    # Role Intelligence API
    # -----------------------------
@app.post("/analyze-role")
async def analyze_role(
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

        detected_role = detect_role(jd_skills)

        role_result = calculate_role_relevance_score(
            resume_skills=resume_skills,
            detected_role=detected_role,
        )

        return {
            "role_analysis": role_result
        }

    # -----------------------------
    # Dynamic Skill Intelligence API
    # -----------------------------
@app.post("/analyze-dynamic-skills")
async def analyze_dynamic_skills(
        resume_file: UploadFile = File(...),
):
        resume_path = os.path.join(UPLOAD_DIR, resume_file.filename)

        with open(resume_path, "wb") as f:
            f.write(await resume_file.read())

        resume_text = parse_resume(resume_path)

        extracted_skills = extract_skills(resume_text)

        # Known skill taxonomy
        from app.skills.skill_list import SKILL_LIST

        # Detect unknown skills
        unknown_skills = detect_unknown_skills(
            extracted_skills=extracted_skills,
            known_skills=SKILL_LIST,
        )

        # Classify unknown skills using AI
        classified_skills = classify_unknown_skills(unknown_skills)

        return {
            "extracted_skills": extracted_skills,
            "unknown_skills": unknown_skills,
            "ai_detected_skills": classified_skills,
        }

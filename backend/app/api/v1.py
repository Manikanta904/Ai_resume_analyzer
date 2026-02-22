import warnings
from app.utils.text_validator import validate_min_words
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional, List, Dict
import os, uuid, datetime


# -----------------------------
# Core imports (your architecture)
# -----------------------------
from app.parsing.resume_parser import parse_resume
from app.parsing.jd_parser import parse_jd
from app.skills.skill_extractor import extract_skills
from app.matching.semantic_matcher import semantic_match


from app.matching.jd_skill_classifier import classify_jd_skills
from app.analysis.experience_analyzer import calculate_experience_score
from app.analysis.project_analyzer import analyze_projects_core
from app.analysis.ats_checker import calculate_ats_format_score


from app.role_intelligence.role_detector import calculate_role_relevance_score, detect_role
from app.analysis.final_scorer import calculate_final_ats_score
from app.analysis.fraud_detector import detect_resume_fraud
from app.ai_engine.section_feedback_ai import generate_section_feedback_ai
from app.ai_engine.skill_fallback import classify_unknown_skills
from app.ai_engine.resume_rewrite_ai import rewrite_resume_for_jd
from app.recruiter.ranking_engine import rank_resumes_against_jd
import warnings
# -----------------------------
# Router
# -----------------------------
router = APIRouter(prefix="/api/v1", tags=["Resume Intelligence"])


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# -----------------------------
# In-memory Resume Version Store
# (replace with DB later)
# -----------------------------
RESUME_VERSIONS: Dict[str, List[Dict]] = {}


# -----------------------------
# Helpers
# -----------------------------
def validate_text_soft(text: str, label: str, validation_warnings: List[str]):
    if not text:
        validation_warnings.append(f"{label} text is empty.")
        return


    if len(text.split()) < 30:
        validation_warnings.append(
            f"{label} text looks short or poorly formatted. Results may be inaccurate."
        )


    validation = validate_min_words(text)
    if not validation["valid"]:
        validation_warnings.append(
            f"{label} text may be too short ({validation['reason']})."
        )




       
def _safe_parse(
    file: Optional[UploadFile],
    text: Optional[str],
    parser_fn,
    label: str,
    validation_warnings: List[str],
) -> str:


    if text:
        validate_text_soft(text, label, validation_warnings)
        return text.strip()




    if not file:
        raise HTTPException(status_code=400, detail=f"{label} required")


    ext = file.filename.split(".")[-1].lower()
    if ext not in ["pdf", "docx", "txt"]:
        raise HTTPException(status_code=400, detail="Unsupported file format")


    path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4()}_{file.filename}")
    with open(path, "wb") as f:
        f.write(file.file.read())


    parsed = parser_fn(path)
    validate_text_soft(parsed, label, validation_warnings)


    return parsed


# ======================================================
# 1️⃣ SINGLE RESUME + SINGLE JD ANALYSIS (MAIN UI)
# ======================================================
@router.post("/analyze")
async def analyze_resume(
    resume_file: Optional[UploadFile] = File(None),
    jd_file: Optional[UploadFile] = File(None),
    resume_text: Optional[str] = Form(None),
    jd_text: Optional[str] = Form(None),
):
    validation_warnings: List[str] = []


    resume_text = _safe_parse(resume_file, resume_text, parse_resume, "Resume", validation_warnings)
    jd_text = _safe_parse(jd_file, jd_text, parse_jd, "Job Description", validation_warnings)


    # ---------- Skills ----------
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)


    # AI fallback for unknown skills
    unknown = list(set(resume_skills) - set(jd_skills))
    if unknown:
        try:
            resume_skills += classify_unknown_skills(unknown)
        except:
            pass


    resume_skills = list(set(resume_skills))


    matched, missing = semantic_match(resume_skills, jd_skills)
    jd_classification = classify_jd_skills(jd_text, jd_skills)


    resume_match_score = int((len(matched) / max(len(jd_skills), 1)) * 100)


    # ---------- Experience ----------
    experience = calculate_experience_score(resume_text, jd_text)
    experience_score = experience.get("experience_score", 0)


    # ---------- Projects ----------
    projects = analyze_projects_core(
    resume_text=resume_text,
    resume_skills=resume_skills,
    jd_skills=jd_skills
)


    project_score = projects.get("project_score", 0)


    # ---------------- ATS + Role ----------------
    ats_format_result = calculate_ats_format_score(resume_text)
    detected_role = detect_role(resume_text)  # STRING

    role_result = calculate_role_relevance_score(
        resume_skills=resume_skills,
        detected_role=detected_role
    )
    role_score = role_result["role_score"]

    # ---------------- Fraud ----------------
    fraud_report = detect_resume_fraud(
        resume_text,
        experience.get("resume_years", 0)
    )

    # ---------------- Final ATS ----------------
    final_ats = calculate_final_ats_score(
        skill_score=resume_match_score,
        experience_score=experience_score,
        project_score=project_score,
        ats_format_score=ats_format_result["ats_format_score"], 
        role_score=role_score,
    )

    # ---------- AI ----------
    ai_feedback = generate_section_feedback_ai(resume_text, jd_text)
    ai_improved = rewrite_resume_for_jd(resume_text, jd_text)


    # ---------- Resume Versions ----------
    resume_id = str(uuid.uuid4())
    RESUME_VERSIONS.setdefault(resume_id, []).append({
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "content": resume_text
    })


    return {
        "resume_id": resume_id,
        "ats_score": final_ats["ats_score"],
        "resume_match_score": resume_match_score,
        "detected_role": detected_role,
        "skills": {
            "matched": matched,
            "missing": missing,
            "must_have": jd_classification["must_have"],
            "good_to_have": jd_classification["good_to_have"],
        },
        "experience": experience,
        "projects": projects,
        "fraud_report": fraud_report,
        "skill_coverage": {
            "matched_percentage": resume_match_score,
            "missing_percentage": 100 - resume_match_score,
        },
        "ai_insights": ai_feedback,
        "ai_resume_improvements": ai_improved,
        "warnings": validation_warnings,
    }


# ======================================================
# 2️⃣ MULTI-JD ANALYSIS (Resume vs many JDs)
# ======================================================
@router.post("/analyze/multi-jd")
async def analyze_multi_jd(
    resume_text: str = Form(...),
    jd_texts: List[str] = Form(...)
):
    validation_warnings = []
    validate_text_soft(resume_text, "Resume", validation_warnings)




    results = []
    for jd in jd_texts:
        validate_text_soft(jd_texts, "Job Description", validation_warnings)


        results.append(await analyze_resume(
            resume_text=resume_text,
            jd_text=jd
        ))


    return {"results": results}


# ======================================================
# 3️⃣ MULTI-RESUME RANKING (Recruiter)
# ======================================================
@router.post("/rank-resumes")
async def rank_resumes(
    resumes: List[str] = Form(...),
    jd_text: str = Form(...)
):
    validation_warnings = []
    validate_text_soft(jd_text, "Job Description", validation_warnings)


    return rank_resumes_against_jd(resumes, jd_text)


# ======================================================
# 4️⃣ RESUME VERSION HISTORY
# ======================================================
@router.get("/resume/{resume_id}/versions")
def get_resume_versions(resume_id: str):
    return RESUME_VERSIONS.get(resume_id, [])






"""
role_detector.py

Enterprise-grade role intelligence engine for ATS systems.
Detects job role from JD and evaluates resume role relevance.
"""

from typing import Dict, List


ROLE_SKILL_MAP = {
    "Backend Developer": [
        "python", "java", "c", "c++", "node", "django", "fastapi",
        "spring", "mysql", "postgresql", "sql", "redis", "docker", "aws"
    ],
    "Frontend Developer": [
        "html", "css", "javascript", "react", "angular", "vue",
        "bootstrap", "tailwind"
    ],
    "Full Stack Developer": [
        "html", "css", "javascript", "react", "node", "django",
        "fastapi", "mysql", "postgresql", "mongodb", "aws"
    ],
    "Data Analyst": [
        "python", "sql", "excel", "powerbi", "tableau",
        "pandas", "numpy"
    ],
    "ML Engineer": [
        "python", "machine learning", "deep learning",
        "tensorflow", "pytorch", "scikit-learn", "nlp"
    ],
    "QA Engineer": [
        "selenium", "cypress", "playwright", "junit",
        "postman", "katalon"
    ],
}


def detect_role(jd_skills: List[str]) -> str:
    """
    Detect job role based on JD skill distribution.
    """
    role_scores = {}

    for role, skills in ROLE_SKILL_MAP.items():
        score = len(set(jd_skills) & set(skills))
        role_scores[role] = score

    detected_role = max(role_scores, key=role_scores.get)

    return detected_role


def calculate_role_relevance_score(
    resume_skills: List[str],
    detected_role: str,
) -> Dict[str, object]:
    """
    Calculate role relevance score based on resume skills.
    """
    required_role_skills = ROLE_SKILL_MAP.get(detected_role, [])

    matched_skills = list(set(resume_skills) & set(required_role_skills))

    if not required_role_skills:
        return {
            "role": detected_role,
            "role_score": 50,
            "matched_role_skills": [],
            "status": "Unknown role taxonomy",
        }

    coverage = len(matched_skills) / len(required_role_skills)

    role_score = int(coverage * 100)

    return {
        "role": detected_role,
        "role_score": role_score,
        "matched_role_skills": matched_skills,
        "status": "Role relevance calculated",
    }

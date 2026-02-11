# app/analysis/section_analyzer.py

import re
from typing import Dict


SECTION_PATTERNS = {
    "summary": r"(summary|profile|about me)(.*?)(experience|projects|skills|education|$)",
    "experience": r"(experience|work experience)(.*?)(projects|skills|education|$)",
    "projects": r"(projects|personal projects|academic projects)(.*?)(skills|education|$)",
    "skills": r"(skills|technical skills)(.*?)(experience|projects|education|$)",
    "education": r"(education|academic)(.*?)(experience|projects|skills|$)",
}


def extract_resume_sections(resume_text: str) -> Dict[str, str]:
    text = resume_text.lower()
    sections = {}

    for section, pattern in SECTION_PATTERNS.items():
        match = re.search(pattern, text, re.DOTALL)
        sections[section] = match.group(2).strip() if match else ""

    return sections

#----------------Section presence & strength analysis-----------
def analyze_section_strength(
    section_text: str,
    jd_skills: list,
) -> str:
    if not section_text:
        return "missing"

    hits = sum(skill.lower() in section_text for skill in jd_skills)

    if hits == 0:
        return "weak"

    if hits < 3:
        return "average"

    return "strong"
#---------------- Main feedback generation function -----------
def generate_section_feedback(
    resume_text: str,
    jd_skills: list,
) -> Dict[str, dict]:

    sections = extract_resume_sections(resume_text)

    feedback = {}

    for section, content in sections.items():
        strength = analyze_section_strength(content, jd_skills)

        feedback[section] = {
            "status": strength,
            "comment": get_section_comment(section, strength),
        }

    return feedback

#---------------- Helper to generate comments -----------
def get_section_comment(section: str, strength: str) -> str:
    if strength == "missing":
        return f"{section.title()} section is missing."
    if strength == "weak":
        return f"{section.title()} section exists but lacks JD relevance."
    if strength == "average":
        return f"{section.title()} section partially matches JD."
    return f"{section.title()} section is well aligned with the JD."

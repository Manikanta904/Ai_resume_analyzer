"""
project_analyzer.py

Industry-grade project relevance analyzer for ATS systems.
Extracts project section from resume and evaluates relevance against JD skills.
"""

import re
from typing import Dict, List


def extract_project_section(resume_text: str) -> str:
    """
    Extract Projects section from resume.
    """
    text = resume_text.lower()

    patterns = [
        r"projects(.+)",
        r"personal projects(.+)",
        r"academic projects(.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1)

    return ""


def extract_project_technologies(project_section: str,
                                 known_skills: List[str]) -> List[str]:
    """
    Detect which technologies are mentioned inside project descriptions.
    """
    detected_skills = []

    for skill in known_skills:
        if skill.lower() in project_section:
            detected_skills.append(skill)

    return list(set(detected_skills))


def calculate_project_relevance_score(
    resume_text: str,
    jd_skills: List[str],
    known_skills: List[str],
) -> Dict[str, object]:
    """
    Calculate project relevance score between resume and JD.
    """
    project_section = extract_project_section(resume_text)

    if not project_section:
        return {
            "project_score": 0,
            "status": "No projects section found in resume",
            "matched_project_skills": [],
        }

    project_tech_stack = extract_project_technologies(
        project_section, known_skills
    )

    matched_skills = list(set(project_tech_stack) & set(jd_skills))

    if not matched_skills:
        return {
            "project_score": 20,
            "status": "Projects found but not relevant to JD",
            "matched_project_skills": [],
        }

    # Each relevant project skill gives 20 points (max 100)
    score = min(100, len(matched_skills) * 20)

    return {
        "project_score": score,
        "status": "Projects relevant to job role",
        "matched_project_skills": matched_skills,
    }

"""
ats_checker.py

Industry-grade ATS format compatibility checker.
Validates resume structure, formatting, and parsing friendliness.
"""

import re
from typing import Dict, List


REQUIRED_SECTIONS = [
    "summary",
    "experience",
    "education",
    "skills",
    "projects",
]


def detect_tables(text: str) -> bool:
    """
    Detect presence of tables (common ATS failure).
    """
    return bool(re.search(r"\|\s*.*\s*\|", text))


def detect_images(text: str) -> bool:
    """
    Detect image references.
    """
    return "image" in text.lower() or "img" in text.lower()


def detect_columns(text: str) -> bool:
    """
    Detect multi-column layouts (approximate detection).
    """
    return bool(re.search(r"\s{4,}\w+", text))


def detect_required_sections(text: str) -> List[str]:
    """
    Detect missing required resume sections.
    """
    text = text.lower()
    missing = []

    for section in REQUIRED_SECTIONS:
        if section not in text:
            missing.append(section)

    return missing


def calculate_ats_format_score(resume_text: str) -> Dict[str, object]:
    """
    Calculate ATS compatibility score and issues.
    """
    issues = []
    score = 100

    # Length check
    word_count = len(resume_text.split())
    if word_count < 300:
        score -= 20
        issues.append("Resume is too short for ATS parsing")

    # Table detection
    if detect_tables(resume_text):
        score -= 20
        issues.append("Tables detected (ATS cannot parse tables)")

    # Image detection
    if detect_images(resume_text):
        score -= 15
        issues.append("Images detected (ATS ignores images)")

    # Column detection
    if detect_columns(resume_text):
        score -= 15
        issues.append("Multi-column layout detected (ATS reads single column)")

    # Section validation
    missing_sections = detect_required_sections(resume_text)
    if missing_sections:
        score -= 20
        issues.append(
            f"Missing required sections: {', '.join(missing_sections)}"
        )

    # Floor score
    score = max(40, score)

    return {
        "ats_format_score": score,
        "word_count": word_count,
        "issues": issues,
        "status": "ATS Friendly" if score >= 75 else "Needs ATS Optimization",
    }

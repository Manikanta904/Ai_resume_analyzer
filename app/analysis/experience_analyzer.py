"""
experience_analyzer.py

Industry-grade experience extraction and scoring engine.
Extracts experience only from Internship / Work Experience sections.
Ignores education timeline.
"""

import re
from datetime import datetime
from typing import Dict


CURRENT_YEAR = datetime.now().year


MONTH_MAP = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}


def extract_experience_section(text: str) -> str:
    """
    Extract only the Internship / Experience section from resume.
    """
    text = text.lower()

    patterns = [
        r"internships(.+)",
        r"experience(.+)",
        r"work experience(.+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1)

    return ""


def extract_years_from_ranges(section_text: str) -> float:
    """
    Extract experience duration from date ranges inside experience section.
    """
    years_found = []

    # Pattern: Aug 2025 - Present, June 2023 - July 2024
    month_year_pattern = (
        r"("
        + "|".join(MONTH_MAP.keys())
        + r")\s+(20\d{2})\s*(?:-|to)\s*(present|"
        + "|".join(MONTH_MAP.keys())
        + r"\s+20\d{2})"
    )

    matches = re.findall(month_year_pattern, section_text)

    for start_month, start_year, end_part in matches:
        start_year = int(start_year)

        if "present" in end_part:
            end_year = CURRENT_YEAR
        else:
            end_year = int(end_part.split()[1])

        duration = max(0, end_year - start_year)
        years_found.append(duration)

    return round(sum(years_found) * 0.5, 1)  # internships weighted as 0.5x


def extract_experience_years(resume_text: str) -> float:
    """
    Extract total experience in years from resume.
    Only counts internships and work experience.
    """
    experience_section = extract_experience_section(resume_text)

    if not experience_section:
        return 0.0

    years = extract_years_from_ranges(experience_section)
    return years


def extract_required_years(jd_text: str) -> float:
    """
    Extract experience requirement from JD.
    """
    jd_text = jd_text.lower()

    matches = re.findall(r"(\d+)\+?\s+years", jd_text)
    if matches:
        return float(max(matches))

    return 0.0


def calculate_experience_score(resume_text: str, jd_text: str) -> Dict[str, object]:
    """
    Calculate experience relevance score between resume and JD.
    """
    resume_years = extract_experience_years(resume_text)
    required_years = extract_required_years(jd_text)

    # Fresher role
    if required_years == 0:
        return {
            "resume_years": resume_years,
            "required_years": 0,
            "experience_score": 100,
            "status": "Fresher role or no experience required",
        }

    if resume_years >= required_years:
        return {
            "resume_years": resume_years,
            "required_years": required_years,
            "experience_score": 100,
            "status": "Meets experience requirement",
        }

    score = int((resume_years / required_years) * 100)

    return {
        "resume_years": resume_years,
        "required_years": required_years,
        "experience_score": score,
        "status": "Below experience requirement",
    }

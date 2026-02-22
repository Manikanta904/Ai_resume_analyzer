"""
resume_versions.py

Resume versioning and ATS score history management.
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List

BASE_DIR = "data/resume_versions"
os.makedirs(BASE_DIR, exist_ok=True)


def generate_resume_id() -> str:
    """Generate unique resume ID."""
    return str(uuid.uuid4())


def get_resume_file_path(resume_id: str) -> str:
    return os.path.join(BASE_DIR, f"{resume_id}.json")


def save_resume_version(
    resume_id: str,
    ats_score: int,
    role: str,
    matched_skills: List[str],
    missing_skills: List[str],
) -> Dict[str, object]:
    """
    Save a new version of resume analysis.
    """

    file_path = get_resume_file_path(resume_id)

    version_data = {
        "version": 1,
        "timestamp": datetime.utcnow().isoformat(),
        "ats_score": ats_score,
        "role": role,
        "summary": {
            "matched_skills": len(matched_skills),
            "missing_skills": len(missing_skills),
        },
    }

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)

        version_data["version"] = len(data["versions"]) + 1
        data["versions"].append(version_data)
    else:
        data = {
            "resume_id": resume_id,
            "versions": [version_data],
        }

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

    return version_data


def get_resume_versions(resume_id: str) -> Dict[str, object]:
    """
    Fetch all versions of a resume.
    """
    file_path = get_resume_file_path(resume_id)

    if not os.path.exists(file_path):
        return {"error": "Resume ID not found"}

    with open(file_path, "r") as f:
        return json.load(f)
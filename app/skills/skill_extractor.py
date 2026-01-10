import re
from app.skills.skill_list import SKILLS
from app.skills.skill_aliases import SKILL_ALIASES
from app.skills.skill_normalizer import normalize_skill


def extract_skills(text: str) -> list[str]:
    text = text.lower()
    found_skills = set()

    # 1️⃣ Detect canonical skills
    for skill in SKILLS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.add(normalize_skill(skill))

    # 2️⃣ Detect aliases directly (CRITICAL FIX)
    for alias, canonical in SKILL_ALIASES.items():
        pattern = r"\b" + re.escape(alias) + r"\b"
        if re.search(pattern, text):
            found_skills.add(normalize_skill(canonical))

    return sorted(found_skills)

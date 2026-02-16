import re
from app.skills.skill_list import SKILL_LIST as SKILLS
from app.skills.skill_aliases import SKILL_ALIASES
from app.skills.skill_normalizer import normalize_skill


def extract_skills(text: str) -> list[str]:
    if not text:
        return []

    text = text.lower()
    found_skills = set()

    def build_pattern(term: str) -> str:
        return r"(?<!\w)" + re.escape(term.lower().strip()) + r"(?!\w)"

    # 1️⃣ Detect canonical skills (longest first to avoid substring clashes)
    sorted_skills = sorted(SKILLS, key=len, reverse=True)

    for skill in sorted_skills:
        pattern = build_pattern(skill)
        if re.search(pattern, text):
            normalized = normalize_skill(skill)
            found_skills.add(normalized)

            # Remove matched text to prevent partial duplicate matches
            text = re.sub(pattern, " ", text)

    # 2️⃣ Detect aliases
    for alias, canonical in SKILL_ALIASES.items():
        pattern = build_pattern(alias)
        if re.search(pattern, text):
            normalized = normalize_skill(canonical)
            found_skills.add(normalized)

            text = re.sub(pattern, " ", text)

    # 3️⃣ Final safety normalization + deduplication
    cleaned = {normalize_skill(skill) for skill in found_skills}

    return sorted(cleaned)

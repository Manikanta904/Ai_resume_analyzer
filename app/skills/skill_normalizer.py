def normalize_skill(skill: str) -> str:
    return skill.lower().strip()
SKILL_NORMALIZATION_MAP = {
    "gen ai": "generative ai",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "selenium webdriver": "selenium",
    "no sql": "nosql",
    "sql scripts": "sql"
}

def normalize_skill(skill: str) -> str:
    return SKILL_NORMALIZATION_MAP.get(skill, skill)

SKILL_NORMALIZATION_MAP = {
    "gen ai": "generative ai",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "selenium webdriver": "selenium",
    "no sql": "nosql",
    "sql scripts": "sql"
}

def normalize_skill(skill: str) -> str:
    skill = skill.lower().strip()
    return SKILL_NORMALIZATION_MAP.get(skill, skill)

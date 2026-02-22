import json
from pathlib import Path
from typing import Dict

CATALOG_PATH = Path("app/data/skill_catalog.json")


def load_skill_catalog() -> Dict:
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_skill_template(skill: str) -> Dict:
    catalog = load_skill_catalog()

    # Skill-specific override if exists
    if skill.lower() in catalog:
        return catalog[skill.lower()]

    # Fallback template (industry standard)
    return catalog["default"]

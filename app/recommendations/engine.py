from typing import List, Dict
from app.recommendations.skill_catalog import get_skill_template


def generate_skill_gap_recommendations(
    missing_skills: List[str]
) -> Dict[str, Dict]:
    """
    Industry-grade skill gap recommendation engine.
    No hardcoded skills.
    No role assumptions.
    """

    recommendations = {}
    for skill in missing_skills:
        template = get_skill_template(skill)

        recommendations[skill] = {
            "learning_path": template.get("learning_path", []),
            "project_ideas": template.get("project_ideas", []),
            "certifications": template.get("certifications", []),
            "confidence": template.get("confidence", "medium")
        }


    return recommendations

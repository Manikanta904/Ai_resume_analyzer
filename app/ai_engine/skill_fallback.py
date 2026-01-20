"""
skill_fallback.py

AI-powered fallback engine using Google Gemini (new SDK).
Used for unknown skill classification.
"""

import os
import json
import re
from typing import List, Dict

from dotenv import load_dotenv
from google import genai

from app.ai_engine.prompts import SKILL_CLASSIFICATION_PROMPT

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


def detect_unknown_skills(
    extracted_skills: List[str],
    known_skills: List[str],
) -> List[str]:
    """
    Detect skills not present in known skill taxonomy.
    """
    known_set = {skill.lower() for skill in known_skills}

    return list(set(
        skill for skill in extracted_skills
        if skill.lower() not in known_set
    ))


def classify_unknown_skills(unknown_skills: List[str]) -> Dict[str, str]:
    """
    Classify unknown skills using Gemini AI.
    Returns a JSON dictionary safely.
    """
    if not unknown_skills:
        return {}

    prompt = SKILL_CLASSIFICATION_PROMPT.format(
        skills=", ".join(unknown_skills)
    )

    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=prompt,
    )

    raw_text = response.text.strip()

    # Remove markdown formatting if present
    cleaned_text = re.sub(r"```json|```", "", raw_text).strip()

    try:
        return json.loads(cleaned_text)
    except json.JSONDecodeError:
        return {
            "error": "AI returned invalid JSON",
            "raw_response": cleaned_text,
        }
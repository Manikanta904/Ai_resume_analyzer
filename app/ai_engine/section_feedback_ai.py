# app/ai_engine/section_feedback_ai.py

import os
import json
from dotenv import load_dotenv
from google import genai

from app.ai_engine.prompts import SECTION_FEEDBACK_PROMPT

load_dotenv()

# Gemini client (same as skill_fallback.py)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_section_feedback_ai(resume_text: str, jd_text: str) -> dict:
    """
    AI-based section-wise resume feedback:
    Summary, Experience, Projects, Skills, Education
    """

    prompt = SECTION_FEEDBACK_PROMPT.format(
        resume_text=resume_text,
        jd_text=jd_text
    )

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt,
    )

    raw_text = response.text.strip()
    raw_text = raw_text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(raw_text)
    except Exception:
        return {
            "summary": {"status": "unknown", "issues": ["LLM parse failed"], "suggestions": []},
            "experience": {"status": "unknown", "issues": ["LLM parse failed"], "suggestions": []},
            "projects": {"status": "unknown", "issues": ["LLM parse failed"], "suggestions": []},
            "skills": {"status": "unknown", "issues": ["LLM parse failed"], "suggestions": []},
            "education": {"status": "unknown", "issues": ["LLM parse failed"], "suggestions": []},
        }



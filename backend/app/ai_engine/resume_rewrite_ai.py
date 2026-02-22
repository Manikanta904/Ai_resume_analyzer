import json
import os
from google import genai
from app.ai_engine.prompts import JD_RESUME_REWRITE_PROMPT

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def rewrite_resume_for_jd(resume_text: str, jd_text: str) -> dict:
    prompt = JD_RESUME_REWRITE_PROMPT.format(
        resume_text=resume_text,
        jd_text=jd_text
    )

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    raw = response.text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(raw)
    except Exception:
        return {
            "summary": "",
            "experience": [],
            "projects": [],
            "error": "Rewrite generation failed"
        }

"""
prompts.py

Central prompt registry for AI engines.
"""

SKILL_CLASSIFICATION_PROMPT = """
You are an ATS skill classification engine.

Given a list of unknown skills extracted from a resume,
classify each skill into one of these categories:

- Programming Language
- Framework / Library
- Cloud / DevOps Tool
- Data / AI Tool
- Testing Tool
- Other Technical Skill

Return JSON only.

Skills:
{skills}
"""

SECTION_FEEDBACK_PROMPT = """
You are an ATS resume reviewer.

Analyze the resume against the job description and provide
section-wise feedback.

Detect:
- Buzzword stuffing
- Vague statements
- Repetition
- Missing JD alignment

Return ONLY valid JSON in this format:

{{
  "summary": {{
    "status": "strong | average | weak | missing",
    "issues": [],
    "suggestions": []
  }},
  "experience": {{
    "status": "strong | average | weak | missing",
    "issues": [],
    "suggestions": []
  }},
  "projects": {{
    "status": "strong | average | weak | missing",
    "issues": [],
    "suggestions": []
  }},
  "skills": {{
    "status": "strong | average | weak | missing",
    "issues": [],
    "suggestions": []
  }}
}}

Resume:
{resume_text}

Job Description:
{jd_text}
"""
JD_RESUME_REWRITE_PROMPT = """
You are an ATS resume optimization engine.

Rewrite the resume ONLY for the given Job Description.

Rules:
- Do NOT add fake experience
- Do NOT increase years of experience
- Use only skills present in resume or JD
- Tailor language strictly to the JD
- Avoid generic buzzwords

Rewrite ONLY these sections:
1. Professional Summary
2. Experience Bullet Points
3. Project Descriptions (if present)

Return STRICT JSON in this format:

{{  
  "summary": "rewritten summary",
  "experience": [
    "bullet 1",
    "bullet 2"
  ],
  "projects": [
    "project rewrite 1"
  ]
}}

Resume:
{resume_text}

Job Description:
{jd_text}
"""

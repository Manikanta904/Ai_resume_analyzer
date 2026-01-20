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

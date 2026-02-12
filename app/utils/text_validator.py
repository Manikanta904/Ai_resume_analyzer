# app/utils/text_validator.py

def validate_min_words(text: str, min_words: int = 20):
    if len(text.strip()) < 300:
        return {
            "valid": False,
            "reason": "LOW_TEXT_LENGTH"
        }
    return {"valid": True}

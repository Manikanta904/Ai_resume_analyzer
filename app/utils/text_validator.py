# app/utils/text_validator.py

def validate_min_words(text: str, min_words: int = 20) -> bool:
    if not text:
        return False

    words = text.strip().split()
    return len(words) >= min_words
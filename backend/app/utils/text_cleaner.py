import re

def clean_text(text: str) -> str:
    """
    Cleans extracted text by removing extra spaces and noise
    """
    if not text:
        return ""

    # Remove multiple newlines
    text = re.sub(r'\n+', '\n', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

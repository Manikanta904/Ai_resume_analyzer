import pdfplumber
from docx import Document

def parse_resume(file_path: str) -> str:
    if file_path.endswith(".pdf"):
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip()
        except Exception:
            # ✅ EDGE CASE: invalid / empty / corrupt PDF
            return ""

    elif file_path.endswith(".docx"):
        try:
            doc = Document(file_path)
            return "\n".join(p.text for p in doc.paragraphs if p.text)
        except Exception:
            return ""

    return ""

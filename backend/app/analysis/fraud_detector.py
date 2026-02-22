# app/analysis/fraud_detector.py

def detect_resume_fraud(skills: list, years_of_experience: int) -> dict:
    flags = []

    if len(skills) > 20 and years_of_experience < 2:
        flags.append("High skill count with low experience")

    if years_of_experience > 15:
        flags.append("Unusually high experience value")

    return {
        "fraud_risk": "high" if flags else "low",
        "signals": flags
    }

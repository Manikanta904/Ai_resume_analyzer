def classify_jd_skills(jd_text: str, jd_skills: list[str]) -> dict:
    text = jd_text.lower()

    must_have = []
    good_to_have = []

    must_section = ""
    good_section = ""

    if "must have" in text:
        must_section = text.split("must have")[1]

    if "good to have" in text:
        good_section = text.split("good to have")[1]

    for skill in jd_skills:
        if skill in must_section:
            must_have.append(skill)
        elif skill in good_section:
            good_to_have.append(skill)
        else:
            good_to_have.append(skill)  # ✅ safer fallback

    return {
        "must_have": list(set(must_have)),
        "good_to_have": list(set(good_to_have))
    }

def calculate_ats_score(
    matched_skills: list[str],
    must_have: list[str],
    good_to_have: list[str]
) -> int:
    score = 0
    max_score = len(must_have) * 2 + len(good_to_have)

    for skill in matched_skills:
        if skill in must_have:
            score += 2
        elif skill in good_to_have:
            score += 1

    if max_score == 0:
        return 0

    ats_score = round((score / max_score) * 100)

    # ✅ DAY 9: Cap perfect score
    ats_score = min(ats_score, 95)

    return ats_score

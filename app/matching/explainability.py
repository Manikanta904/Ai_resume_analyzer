def explain_score(matched, must_have, good_to_have):
    explanation = []

    for skill in must_have:
        if skill in matched:
            explanation.append(f"{skill}: matched (must-have)")
        else:
            explanation.append(f"{skill}: missing (must-have)")

    for skill in good_to_have:
        if skill in matched:
            explanation.append(f"{skill}: matched (good-to-have)")
        else:
            explanation.append(f"{skill}: missing (good-to-have)")

    return explanation

def calculate_ats_score(matched: list[str], total_required: int) -> int:
    if total_required == 0:
        return 0
    return round((len(matched) / total_required) * 100)

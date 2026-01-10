from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_match(resume_skills, jd_skills, threshold=0.80):
    res_emb = model.encode(resume_skills)
    jd_emb = model.encode(jd_skills)

    matched = set()
    missing = set(jd_skills)

    for i, jd_skill in enumerate(jd_skills):
        for j, res_skill in enumerate(resume_skills):
            score = cosine_similarity(
                [jd_emb[i]],
                [res_emb[j]]
            )[0][0]

            if score >= threshold:
                matched.add(jd_skill)
                missing.discard(jd_skill)
                break

    return {
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing)
    }

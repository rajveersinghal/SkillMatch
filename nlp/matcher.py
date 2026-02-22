from sklearn.metrics.pairwise import cosine_similarity

def calculate_match_score(tfidf_vectors):
    """
    Calculates similarity score (0–100%) between resume and JD.
    """
    similarity = cosine_similarity(
        tfidf_vectors[0],
        tfidf_vectors[1]
    )

    score = similarity[0][0] * 100
    return round(score, 2)

def identify_skill_gap(resume_skills: list[str], jd_skills: list[str]) -> list[str]:
    """
    Identifies missing skills: jd_skills - resume_skills
    """
    return sorted(list(set(jd_skills) - set(resume_skills)))

def group_skills_by_category(missing_skills, taxonomy):
    """
    Groups missing skills into predefined categories.
    """
    grouped_skills = {}

    for category, skills in taxonomy.items():
        matched = [skill for skill in missing_skills if skill in skills]
        if matched:
            grouped_skills[category] = matched

    return grouped_skills

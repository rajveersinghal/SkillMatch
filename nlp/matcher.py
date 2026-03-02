import math

def calculate_match_score(tfidf_vectors):
    """
    Calculates similarity score (0–100%) between resume and JD.
    """
    vec1, vec2 = tfidf_vectors[0], tfidf_vectors[1]
    
    # Cosine Similarity between two dict vectors
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
    if not denominator:
        score = 0.0
    else:
        score = (float(numerator) / denominator) * 100
        
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

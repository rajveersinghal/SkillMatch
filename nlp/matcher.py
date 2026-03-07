import os
import threading

# Initialize the model lazily. Using all-MiniLM-L6-v2 for speed/quality balance.
_model = None
_model_lock = threading.Lock()

def get_model():
    global _model
    with _model_lock:
        if _model is None:
            print("DEBUG: Importing sentence_transformers...")
            from sentence_transformers import SentenceTransformer
            print("DEBUG: Loading SentenceTransformer model 'all-MiniLM-L6-v2'...")
            _model = SentenceTransformer('all-MiniLM-L6-v2')
            print("DEBUG: SentenceTransformer model loaded successfully.")
    return _model

def calculate_match_score_semantic(resume_text: str, jd_text: str) -> float:
    """
    Calculates semantic similarity score (0–100%) using Sentence-Transformers.
    This captures intent and meaning, not just keyword overlap.
    """
    if not resume_text or not jd_text:
        return 0.0
        
    model = get_model()
    from sentence_transformers import util
    
    # Encode both texts
    embeddings1 = model.encode(resume_text, convert_to_tensor=True)
    embeddings2 = model.encode(jd_text, convert_to_tensor=True)
    
    # Compute cosine similarity
    cosine_scores = util.cos_sim(embeddings1, embeddings2)
    
    # Convert back to percentage (0.0 to 1.0 -> 0 to 100)
    score = float(cosine_scores[0][0]) * 100
    
    # Clip to 0-100 just in case
    score = max(0, min(100, score))
    
    return round(score, 2)

def calculate_match_score(tfidf_vectors):
    """
    DEPRECATED: Keeping signature for backward compatibility until pipeline is fully shifted.
    Calculates similarity score (0–100%) between resume and JD using TF-IDF.
    """
    import math
    vec1, vec2 = tfidf_vectors[0], tfidf_vectors[1]
    
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    
    if not denominator:
        return 0.0
    return round((float(numerator) / denominator) * 100, 2)

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

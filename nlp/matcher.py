import os
import threading
import re

def calculate_match_score_semantic(resume_text: str, jd_text: str) -> float:
    """
    Lightweight keyword overlap (Jaccard similarity proxy)
    to prevent out-of-memory errors on Render.
    """
    if not resume_text or not jd_text:
        return 0.0
        
    # Convert to lowercase words for simple matching
    resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
    jd_words = set(re.findall(r'\b\w+\b', jd_text.lower()))
    
    if not jd_words:
        return 0.0
        
    # Calculate simple overlap percentage of JD words found in resume
    overlap = jd_words.intersection(resume_words)
    score = (len(overlap) / len(jd_words)) * 100.0
    
    # Clip to 0-100 just in case
    score = max(0, min(100, score))
    
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

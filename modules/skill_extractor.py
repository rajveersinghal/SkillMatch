import pandas as pd

def load_skills():
    skills_df = pd.read_csv("data/skills_db.csv", header=None)
    skills = skills_df[0].str.lower().tolist()
    return skills

import re

def extract_skills(text, skills):
    # Escape special characters in skills (e.g., "C++", "C#", ".NET")
    # Sort by length descending to match longer phrases first (e.g., "Machine Learning" before "Machine")
    sorted_skills = sorted(skills, key=len, reverse=True)
    
    extracted = []
    
    text_lower = text.lower()
    
    for skill in sorted_skills:
        # Simple word boundary check doesn't work well for C++ etc.
        # Let's use a robust approach: check if the skill exists as a distinct word
        # (?:^|[\s,.\(\)/]) matches start of string or a separator
        pattern = r'(?:^|[\s,.\(\)/])' + re.escape(skill) + r'(?:$|[\s,.\(\)/])'
        
        if re.search(pattern, text_lower):
             extracted.append(skill)
             
    return list(set(extracted))

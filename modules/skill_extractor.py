import pandas as pd

def load_skills():
    skills_df = pd.read_csv("data/skills_db.csv", header=None)
    skills = skills_df[0].str.lower().tolist()
    return skills

def extract_skills(text, skills):
    extracted = []
    for skill in skills:
        if skill in text:
            extracted.append(skill)
    return list(set(extracted))

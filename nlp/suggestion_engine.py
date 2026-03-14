import os
import logging
import math
from app_data.skill_taxonomy import skill_taxonomy

# Co-occurrence map: If JD has Key, suggest Values if they are missing from Resume
CO_OCCURRENCE_MAP = {
    "python": ["numpy", "pandas", "matplotlib", "seaborn"],
    "machine learning": ["scikit-learn", "scipy", "xgboost"],
    "deep learning": ["tensorflow", "pytorch", "keras"],
    "sql": ["postgresql", "mysql", "mongodb"],
    "javascript": ["react", "node.js", "typescript"],
    "data science": ["statistics", "data cleaning", "eda"]
}

class SuggestionEngine:
    def __init__(self):
        # Flatten taxonomy for search
        self.all_taxonomy_skills = []
        for cat_skills in skill_taxonomy.values():
            self.all_taxonomy_skills.extend(cat_skills)
        self.all_taxonomy_skills = list(set(self.all_taxonomy_skills))
    def suggest_cooccurrence(self, jd_skills, resume_skills):
        """Method 1: Suggest skills based on JD skills"""
        suggestions = []
        for skill in jd_skills:
            if skill.lower() in CO_OCCURRENCE_MAP:
                suggestions.extend(CO_OCCURRENCE_MAP[skill.lower()])
        # Filter out what's already in the resume (optional but usually good)
        resume_lower = [s.lower() for s in resume_skills]
        return list(set([s for s in suggestions if s.lower() not in resume_lower]))

    def suggest_embeddings(self, jd_skills, resume_skills):
        """Method 2: Placeholder for semantic/embedding based suggestions"""
        # In a full implementation, this might use vector search
        # For now, we return placeholder related skills from taxonomy
        return ["keras", "pytorch", "tensorflow"] if "deep learning" in [s.lower() for s in jd_skills] else []

    def get_all_suggestions(self, jd_skills, resume_skills):
        """Combine all suggestion methods"""
        co_sug = self.suggest_cooccurrence(jd_skills, resume_skills)
        emb_sug = self.suggest_embeddings(jd_skills, resume_skills)
        return list(set(co_sug + emb_sug))

    def get_actionable_roadmap(self, missing_skills):
        """Method 3: Generate actionable learning roadmap for missing skills"""
        roadmap = []
        
        # Hardcoded dictionary for MVP, can be expanded to a DB/external API
        resource_map = {
            "react": {"url": "https://react.dev/learn", "time": "2 weeks", "type": "Documentation"},
            "python": {"url": "https://docs.python.org/3/tutorial/", "time": "3 weeks", "type": "Tutorial"},
            "machine learning": {"url": "https://www.coursera.org/learn/machine-learning", "time": "8 weeks", "type": "Course"},
            "sql": {"url": "https://www.w3schools.com/sql/", "time": "1 week", "type": "Interactive"},
            "javascript": {"url": "https://javascript.info/", "time": "2 weeks", "type": "Guide"},
            "docker": {"url": "https://docs.docker.com/get-started/", "time": "1 week", "type": "Documentation"},
            "aws": {"url": "https://aws.amazon.com/training/", "time": "4 weeks", "type": "Certification Path"},
            "node.js": {"url": "https://nodejs.dev/learn", "time": "2 weeks", "type": "Tutorial"},
            "pandas": {"url": "https://pandas.pydata.org/docs/user_guide/10min.html", "time": "3 days", "type": "Documentation"},
            "git": {"url": "https://git-scm.com/book/en/v2", "time": "3 days", "type": "Book"}
        }

        for skill in missing_skills:
            lower_skill = skill.lower()
            if lower_skill in resource_map:
                info = resource_map[lower_skill]
                roadmap.append({
                    "skill": skill,
                    "url": info["url"],
                    "estimated_time": info["time"],
                    "resource_type": info["type"]
                })
            else:
                roadmap.append({
                    "skill": skill,
                    "url": f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+tutorial",
                    "estimated_time": "Varies",
                    "resource_type": "Video Search"
                })
                
        return roadmap

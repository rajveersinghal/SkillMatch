import os
import logging
import math
from nlp.vectorizer import SimpleTfidfVectorizer
from nlp.matcher import calculate_match_score
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
        
        # Initialize Vectorizer
        self.vectorizer = SimpleTfidfVectorizer()

    def suggest_cooccurrence(self, jd_skills, resume_skills):
        """Method 1: Co-occurrence based suggestions"""
        suggestions = []
        resume_skills_set = set(s.lower() for s in resume_skills)
        jd_skills_set = set(s.lower() for s in jd_skills)
        
        for key, recs in CO_OCCURRENCE_MAP.items():
            if key in jd_skills_set:
                for rec in recs:
                    if rec not in resume_skills_set:
                        suggestions.append(rec)
        
        return list(set(suggestions))

    def suggest_embeddings(self, jd_skills, resume_skills, top_k=3):
        """Method 2: Similarity based suggestions for semantically similar skills"""
        resume_skills_set = set(s.lower() for s in resume_skills)
        # Skills in taxonomy that the user DOES NOT have
        potential_skills = [s for s in self.all_taxonomy_skills if s not in resume_skills_set]
        
        if not potential_skills or not jd_skills:
            return []

        try:
            # Pairwise similarity: Extract similarity between JD skills and Taxonomy skills
            # We fit on the union of both to have a shared vocabulary
            corpus = jd_skills + potential_skills
            vectors = self.vectorizer.fit_transform(corpus)
            
            # Split matrix back into JD and Potential
            jd_vectors = vectors[:len(jd_skills)]
            potential_vectors = vectors[len(jd_skills):]

            suggestions = []
            for i in range(len(jd_skills)):
                scores = []
                for j in range(len(potential_skills)):
                    score = calculate_match_score([jd_vectors[i], potential_vectors[j]])
                    scores.append((score, potential_skills[j]))
                
                # Sort descending
                scores.sort(key=lambda x: x[0], reverse=True)
                
                for k in range(min(top_k, len(scores))):
                    if scores[k][0] > 30.0:  # 30% similarity threshold
                        suggestions.append(scores[k][1])
            
            return list(set(suggestions))
        except Exception as e:
            logging.error(f"Suggestion Engine Error: {str(e)}")
            return []

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

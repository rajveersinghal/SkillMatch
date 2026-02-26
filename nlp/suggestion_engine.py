import os

# Suppress HuggingFace and Transformers verbose logging before imports
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

import logging
# Completely silence the 'unauthenticated requests' warning from huggingface_hub
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("sentence_transformers").setLevel(logging.ERROR)

# Set transformers logging to error only to hide 'UNEXPECTED' weight reports
from transformers import logging as transformers_logging
transformers_logging.set_verbosity_error()

from sentence_transformers import SentenceTransformer, util
import torch
from data.skill_taxonomy import skill_taxonomy

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
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        # Only load model if needed for performance
        self.model_name = model_name
        self.model = None
        
        # Flatten taxonomy for embedding search
        self.all_taxonomy_skills = []
        for cat_skills in skill_taxonomy.values():
            self.all_taxonomy_skills.extend(cat_skills)
        self.all_taxonomy_skills = list(set(self.all_taxonomy_skills))

    def _load_model(self):
        if self.model is None:
            # Suppress loading progress bars
            self.model = SentenceTransformer(self.model_name)
            # Disable progress bar globally for this instance if needed, 
            # though show_progress_bar is usually an argument in encode()
            # The weight loading bar is harder to suppress without setting HF_HUB_OFFLINE=1
            # but we can try setting the verbosity of the Hub.
            import huggingface_hub
            huggingface_hub.utils.logging.set_verbosity_error()

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
        """Method 2: Embedding based suggestions for semantically similar skills"""
        self._load_model()
        
        resume_skills_set = set(s.lower() for s in resume_skills)
        # Skills in taxonomy that the user DOES NOT have
        potential_skills = [s for s in self.all_taxonomy_skills if s not in resume_skills_set]
        
        if not potential_skills or not jd_skills:
            return []

        # Encode JD skills and potential skills without progress bars
        jd_embeddings = self.model.encode(jd_skills, convert_to_tensor=True, show_progress_bar=False)
        potential_embeddings = self.model.encode(potential_skills, convert_to_tensor=True, show_progress_bar=False)

        # Calculate cosine similarity
        cosine_scores = util.cos_sim(jd_embeddings, potential_embeddings)
        
        # For each JD skill, find top similar skills user doesn't have
        suggestions = []
        for i in range(len(jd_skills)):
            # Get indices of top_k highest scores for this JD skill
            top_results = torch.topk(cosine_scores[i], k=min(top_k, len(potential_skills)))
            
            for score, idx in zip(top_results[0], top_results[1]):
                if score > 0.6: # threshold for similarity
                    suggestions.append(potential_skills[idx])
        
        return list(set(suggestions))

    def get_all_suggestions(self, jd_skills, resume_skills):
        co_occ = self.suggest_cooccurrence(jd_skills, resume_skills)
        embeds = self.suggest_embeddings(jd_skills, resume_skills)
        
        # Merge and remove duplicates
        all_sug = list(set(co_occ + embeds))
        # Remove skills already in JD (since they are already "missing skills")
        jd_skills_set = set(s.lower() for s in jd_skills)
        all_sug = [s for s in all_sug if s not in jd_skills_set]
        
        return all_sug

from nlp.suggestion_engine import SuggestionEngine

def test_cooccurrence_suggestions():
    engine = SuggestionEngine()
    jd_skills = ["python", "machine learning"]
    resume_skills = ["python"]
    
    suggestions = engine.suggest_cooccurrence(jd_skills, resume_skills)
    
    # Python trigger: numpy, pandas, matplotlib, seaborn
    # ML trigger: scikit-learn, scipy, xgboost
    # Since resume has python, numpy/pandas/etc should be suggested
    # Since resume doesn't have ML, scikit-learn/etc should be suggested
    
    assert "numpy" in suggestions or "pandas" in suggestions
    assert "scikit-learn" in suggestions

def test_embedding_suggestions():
    engine = SuggestionEngine()
    jd_skills = ["Deep Learning"]
    resume_skills = ["Python"]
    
    suggestions = engine.suggest_embeddings(jd_skills, resume_skills)
    
    # Deep Learning is semantically close to keras, pytorch, tensorflow in our taxonomy
    assert any(s in ["keras", "pytorch", "tensorflow"] for s in suggestions)

def test_all_suggestions():
    engine = SuggestionEngine()
    jd_skills = ["SQL", "JavaScript"]
    resume_skills = ["SQL", "React"]
    
    all_sug = engine.get_all_suggestions(jd_skills, resume_skills)
    
    # SQL -> postgresql, mysql, mongodb
    # JavaScript -> react, node.js, typescript
    # Resume already has React, so node.js/typescript should be suggested
    
    assert "node.js" in all_sug or "typescript" in all_sug
    assert "postgresql" in all_sug or "mysql" in all_sug

if __name__ == "__main__":
    # Simple manual run
    test_cooccurrence_suggestions()
    test_embedding_suggestions()
    test_all_suggestions()
    print("✅ All suggestion tests passed!")

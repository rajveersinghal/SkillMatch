from sklearn.feature_extraction.text import TfidfVectorizer

def generate_tfidf_vectors(resume_text: str, jd_text: str):
    """
    Converts resume and job description text into TF-IDF vectors.
    
    Parameters:
    resume_text (str): Preprocessed resume text.
    jd_text (str): Preprocessed job description text.
    
    Returns:
    tuple: (vectors, vectorizer)
           vectors: Sparse matrix of TF-IDF vectors (Shape: 2 x N)
           vectorizer: Fitted TfidfVectorizer object
    """
    # Initialize TF-IDF Vectorizer
    # max_features=5000: Limits vocabulary to top 5000 terms to control dimensionality
    # ngram_range=(1, 2): Captures unigrams (single words) and bigrams (two-word phrases like 'machine learning')
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2)
    )

    # Fit and transform the texts
    # We treat resume and JD as a small corpus of 2 documents for this pairwise comparison
    # In a full search system, the vectorizer would be fitted on a larger corpus.
    vectors = vectorizer.fit_transform([resume_text, jd_text])

    return vectors, vectorizer

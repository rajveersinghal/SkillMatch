import math
from collections import Counter
import re

class SimpleTfidfVectorizer:
    def __init__(self):
        self.vocab = set()
        self.idf = {}

    def _get_ngrams(self, text, n=1):
        tokens = re.findall(r'\b\w+\b', text.lower())
        ngrams = []
        for i in range(len(tokens) - n + 1):
            ngrams.append(" ".join(tokens[i:i+n]))
        return ngrams

    def fit_transform(self, documents):
        doc_tokens = []
        for doc in documents:
            tokens = self._get_ngrams(doc, 1) + self._get_ngrams(doc, 2)
            doc_tokens.append(tokens)
            self.vocab.update(tokens)
            
        N = len(documents)
        for term in self.vocab:
            df = sum(1 for tokens in doc_tokens if term in tokens)
            self.idf[term] = math.log((1 + N) / (1 + df)) + 1

        vectors = []
        for tokens in doc_tokens:
            counts = Counter(tokens)
            vec = {}
            for term, count in counts.items():
                tf = count
                vec[term] = tf * self.idf[term]
                
            norm = math.sqrt(sum(v**2 for v in vec.values()))
            if norm > 0:
                for term in vec:
                    vec[term] /= norm
            vectors.append(vec)
            
        return vectors

def generate_tfidf_vectors(resume_text: str, jd_text: str):
    """
    Converts resume and job description text into TF-IDF vectors using pure Python.
    """
    vectorizer = SimpleTfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    return vectors, vectorizer

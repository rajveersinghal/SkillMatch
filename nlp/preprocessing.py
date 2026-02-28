import re
import os
import spacy
import nltk
from nltk.corpus import stopwords

# Configure NLTK to use /tmp if on Vercel
if os.getenv("VERCEL"):
    nltk.data.path.append("/tmp/nltk_data")

# Download once (safe to run multiple times, checks existence)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    try:
        nltk.download("stopwords", download_dir="/tmp/nltk_data" if os.getenv("VERCEL") else None)
    except Exception as e:
        print(f"NLTK Download Warning: {e}")

# Load resources
# Model is pre-installed via requirements.txt
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    print(f"Error: SpaCy model 'en_core_web_sm' not found. Ensure it is in requirements.txt. Detail: {e}")
    # Fallback to a dummy object to prevent total crash on startup
    class DummyNLP:
        def __call__(self, text): return []
    nlp = DummyNLP()

STOP_WORDS = set(stopwords.words("english"))

def preprocess_text(text: str) -> str:
    """
    Cleans and normalizes input text using spaCy and NLTK.
    1. Lowercase
    2. Remove special characters & digits
    3. Tokenization + Lemmatization + Stopword removal
    """
    if not text or not isinstance(text, str):
        return ""

    # 1. Lowercase
    text = text.lower()

    # 2. Remove special characters & digits (keep only a-z and whitespace)
    text = re.sub(r"[^a-z\s]", " ", text)

    # 3. Tokenization + Lemmatization
    doc = nlp(text)

    tokens = []
    for token in doc:
        # Filter: not a stopword, length > 2, not whitespace
        if (
            token.text not in STOP_WORDS
            and len(token.text) > 2
            and not token.is_space
        ):
            tokens.append(token.lemma_)

    return " ".join(tokens)

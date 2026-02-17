import re
import spacy
import nltk
from nltk.corpus import stopwords

# Download once (safe to run multiple times, checks existence)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download("stopwords")

# Load resources
# Ensure 'en_core_web_sm' is downloaded before running this
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

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

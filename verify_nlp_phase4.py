from nlp.vectorizer import generate_tfidf_vectors

print("--- TF-IDF Verification ---")

resume_sample = "python sql machine learning pandas"
jd_sample = "python machine learning deep learning sql"

print(f"Resume: {resume_sample}")
print(f"JD: {jd_sample}")

vectors, vectorizer = generate_tfidf_vectors(resume_sample, jd_sample)

print(f"\nVector Shape: {vectors.shape}")
print(f"Sample Features: {vectorizer.get_feature_names_out()[:10]}")

# Verification checks
if vectors.shape[0] == 2:
    print("✅ Shape Check Passed (2 documents)")
else:
    print("❌ Shape Check Failed")

features = vectorizer.get_feature_names_out()
expected_snippets = ['machine', 'learning', 'machine learning', 'python']
if all(term in features for term in expected_snippets):
    print("✅ Feature Extraction Check Passed (includes bigrams)")
else:
    print(f"❌ Feature Extraction Failed. Got: {features}")

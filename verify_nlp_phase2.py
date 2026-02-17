from nlp.preprocessing import preprocess_text

sample = "Experienced Data Scientist with 3+ years of experience in Python, SQL & Machine Learning."
processed = preprocess_text(sample)
print(f"Original: {sample}")
print(f"Processed: {processed}")

expected_snippets = ["experience", "data", "scientist", "python", "sql", "machine", "learning"]
if all(snippet in processed for snippet in expected_snippets):
    print("✅ Pipeline Verification Passed")
else:
    print("❌ Pipeline Verification Failed")

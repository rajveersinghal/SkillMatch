from nlp.skill_extractor import extract_skills

sample_text = "Experienced in Python, SQL, Pandas, Machine Learning and Streamlit."
print(f"Sample Text: {sample_text}")

extracted = extract_skills(sample_text)
print(f"Extracted Skills: {extracted}")

expected = ['machine learning', 'pandas', 'python', 'sql', 'streamlit']
# Note: output is sorted
if extracted == expected:
    print("✅ Skill Extraction Verification Passed")
else:
    print(f"❌ Skill Extraction Verification Failed. Expected {expected}, but got {extracted}")

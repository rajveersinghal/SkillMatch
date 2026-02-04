import streamlit as st
from modules.resume_parser import extract_resume_text
from modules.jd_parser import extract_jd_text
from modules.text_cleaner import clean_text
from modules.skill_extractor import load_skills, extract_skills

# Page configuration
st.set_page_config(
    page_title="SkillMatch AI",
    layout="centered"
)

# Title
st.title("📄 SkillMatch – Resume Matcher & Skill Recommender")

st.write(
    "Upload your resume and paste the job description to analyze skill match."
)

# Load skills
skills = load_skills()
st.write(f"Total Skills Loaded: {len(skills)}")

# Resume upload
st.subheader("Upload Resume")
resume_file = st.file_uploader(
    "Upload your resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

# Job description input
st.subheader("Job Description")
job_description = st.text_area(
    "Paste the job description here",
    height=200
)

# Analyze button
if st.button("Analyze Resume"):
    if resume_file and job_description:
        resume_text = extract_resume_text(resume_file)

        st.subheader("Extracted Resume Text")
        st.write(resume_text[:1000])  # preview first 1000 chars

        jd_text = extract_jd_text(job_description)
        st.subheader("Job Description Text")
        st.write(jd_text[:1000])

        clean_resume = clean_text(resume_text)
        clean_jd = clean_text(jd_text)

        st.subheader("Cleaned Resume Text")
        st.write(clean_resume[:800])

        st.subheader("Cleaned Job Description Text")
        st.write(clean_jd[:800])

        resume_skills = extract_skills(clean_resume, skills)
        jd_skills = extract_skills(clean_jd, skills)

        st.subheader("🔍 Skills Found in Resume")
        st.write(resume_skills)

        st.subheader("📌 Skills Required in Job Description")
        st.write(jd_skills)

        st.success("Inputs received successfully!")
    else:
        st.warning("Please upload a resume and enter a job description.")

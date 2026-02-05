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
        jd_text = extract_jd_text(job_description)

        clean_resume = clean_text(resume_text)
        clean_jd = clean_text(jd_text)

        resume_skills = set(extract_skills(clean_resume, skills))
        jd_skills = set(extract_skills(clean_jd, skills))

        # --- Match Logic ---
        matched_skills = resume_skills.intersection(jd_skills)
        missing_skills = jd_skills - resume_skills
        
        # Calculate Match Score
        if len(jd_skills) > 0:
            match_score = (len(matched_skills) / len(jd_skills)) * 100
        else:
            match_score = 0

        # --- Display Results ---
        
        st.divider()
        st.subheader("📊 Skill Match Results")
        
        # Score Metric
        st.metric(label="Match Score", value=f"{match_score:.1f}%")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"✅ Matched Skills ({len(matched_skills)})")
            if matched_skills:
                for skill in matched_skills:
                     st.write(f"- {skill.title()}")
            else:
                st.write("No matching skills found.")

        with col2:
            st.warning(f"⚠️ Missing Skills ({len(missing_skills)})")
            if missing_skills:
                 for skill in missing_skills:
                     st.write(f"- {skill.title()}")
            else:
                st.write("Great! You have all the required skills.")
        
        st.divider()
        
        # Show raw list if needed (expander)
        with st.expander("See Extracted Data Details"):
            st.write("**Resume Skills Found:**", list(resume_skills))
            st.write("**JD Skills Required:**", list(jd_skills))
            st.write("**Cleaned Resume Text:**", clean_resume[:500] + "...")
            st.write("**Cleaned JD Text:**", clean_jd[:500] + "...")

    else:
        st.warning("Please upload a resume and enter a job description.")

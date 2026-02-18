import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
try:
    import frontend.api_client as api
except ImportError:
    import api_client as api

from core.ingestion import extract_text
from nlp.preprocessing import preprocess_text
from nlp.skill_extractor import extract_skills




# Page Config
st.set_page_config(page_title="SkillMatch - Resume Matcher", layout="wide", page_icon="🧩")

# --- Custom CSS Injection ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    local_css("frontend/style.css")
except FileNotFoundError:
    # Fallback if running from a different directory context
    try:
        local_css("style.css") 
    except:
        st.warning("CSS file not found. UI styling might be missing.")


if "token" not in st.session_state:
    st.session_state.token = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# --- Helper Functions for UI ---
def display_skill_tags(skills, skill_type="neutral"):
    """
    Display skills as styled tags.
    skill_type: 'neutral', 'match', 'missing'
    """
    color_class = ""
    if skill_type == "match":
        color_class = "match"
    elif skill_type == "missing":
        color_class = "missing"
    
    html = ""
    for skill in skills:
        html += f'<span class="skill-tag {color_class}">{skill}</span>'
    st.markdown(html, unsafe_allow_html=True)

# --- Main App Logic ---

if not st.session_state.token:
    # Centered Login/Register
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🧩 SkillMatch")
        st.markdown("### Intelligent Resume vs. Job Description Matcher")
        st.info("Please log in or register to verify and track your resume matches.")
        
        tab1, tab2 = st.tabs(["🔒 Login", "📝 Register"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", use_container_width=True)
                
                if submit:
                    data = api.login(email, password)
                    if data and "access_token" in data:
                        st.session_state.token = data["access_token"]
                        st.session_state.user_email = email
                        st.success("Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please try again.")

        with tab2:
            with st.form("register_form"):
                reg_email = st.text_input("Email")
                reg_pass = st.text_input("Create Password", type="password")
                reg_submit = st.form_submit_button("Register", use_container_width=True)
                
                if reg_submit:
                    if api.register(reg_email, reg_pass):
                        st.success("✅ Registration successful! Please switch to the Login tab.")
                    else:
                        st.error("Registration failed. User might already exist.")

else:
    # Sidebar Navigation
    with st.sidebar:
        st.title("🧩 SkillMatch")
        st.markdown(f"**User**: `{st.session_state.user_email}`")
        st.divider()
        page = st.radio("Navigate", ["📂 Upload & Analyze", "📜 History", "🚪 Logout"])
        
        st.divider()
        st.info("💡 **Tip**: Use the 'History' tab to view past analyses.")

    if page == "📂 Upload & Analyze":
        st.title("Analyze Your Resume")
        st.markdown("Upload your Resume and a Job Description to see how well they match and identify missing skills.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📄 Resume")
            resume_file = st.file_uploader("Upload PDF/DOCX", type=["pdf", "docx"], key="resume_uploader")
            resume_text_manual = st.text_area("Or paste text here...", height=200, key="resume_manual")
        
        with col2:
            st.subheader("💼 Job Description")
            jd_file = st.file_uploader("Upload PDF/DOCX", type=["pdf", "docx"], key="jd_uploader")
            jd_text_manual = st.text_area("Or paste text here...", height=200, key="jd_manual")
        
        st.divider()
        
        analyze_col1, analyze_col2, analyze_col3 = st.columns([1, 2, 1])
        with analyze_col2:
            submit_button = st.button("🚀 Analyze Compatibility", type="primary", use_container_width=True)

        if submit_button:
            # 1. Extraction
            resume_text = ""
            if resume_file:
                resume_text = extract_text(resume_file)
            elif resume_text_manual:
                resume_text = resume_text_manual
            
            job_description = ""
            if jd_file:
                job_description = extract_text(jd_file)
            elif jd_text_manual:
                job_description = jd_text_manual
            
            if resume_text and job_description:
                with st.spinner("🔍 Analyzing documents and extracting skills..."):
                    # 2. Processing
                    processed_resume = preprocess_text(resume_text)
                    processed_jd = preprocess_text(job_description)
                    
                    resume_skills = extract_skills(processed_resume)
                    jd_skills = extract_skills(processed_jd)
                    
                    # 3. Backend Submission
                    api_success = api.upload_document(st.session_state.token, resume_text, job_description)
                
                if api_success:
                    st.success("✅ Documents processed & saved!")
                else:
                    st.warning("⚠️ Analysis complete, but failed to save to history.")

                # 4. Results Display
                st.divider()
                st.header("📊 Analysis Results")

                # Metrics Row
                m_col1, m_col2, m_col3 = st.columns(3)
                
                # Calculations
                missing_skills = sorted(list(set(jd_skills) - set(resume_skills)))
                matching_skills = sorted(list(set(jd_skills) & set(resume_skills)))
                match_percentage = 0
                if jd_skills:
                    match_percentage = int((len(matching_skills) / len(jd_skills)) * 100)
                
                with m_col1:
                    st.metric("Match Score", f"{match_percentage}%")
                    st.progress(match_percentage / 100)
                with m_col2:
                    st.metric("Matching Skills", len(matching_skills))
                with m_col3:
                    st.metric("Missing Skills", len(missing_skills))

                # Skills Visuals
                c1, c2 = st.columns(2)
                with c1:
                    st.subheader("✅ Matching Skills")
                    if matching_skills:
                        display_skill_tags(matching_skills, "match")
                    else:
                        st.info("No matching skills found.")
                        
                with c2:
                    st.subheader("❌ Missing Skills")
                    if missing_skills:
                        display_skill_tags(missing_skills, "missing")
                    else:
                        st.success("No missing skills! You're a great fit.")

                st.subheader("📋 Detected Resume Skills")
                display_skill_tags(resume_skills, "neutral")

                # Debug / Detailed View - REMOVED as per user request


            else:
                st.error("❌ Please provide both Resume and Job Description.")

    elif page == "📜 History":
        st.title("Submission History")
        docs = api.get_documents(st.session_state.token)
        
        if docs:
            for i, doc in enumerate(docs):
                # Using a container for card-like styling
                with st.container():
                    st.markdown(f"""
                    <div class="history-card">
                        <div class="history-header">
                            <strong>Submission #{len(docs) - i}</strong>
                            <span class="history-date">{doc.get('created_at', 'Date Unknown')}</span>
                        </div>
                        <p style="color: #64748B; font-size: 0.9em; margin-bottom: 0.5rem;">
                            <strong>Resume Preview:</strong> {doc.get('resume_text', '')[:100]}...
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander("View Full Details", expanded=False):
                        h_col1, h_col2 = st.columns(2)
                        with h_col1:
                            st.subheader("Restored Resume Skills")
                            if "resume_skills" in doc and doc["resume_skills"]:
                                display_skill_tags(doc["resume_skills"], "neutral")
                            else:
                                st.caption("No skills stored.")
                        with h_col2:
                            st.subheader("Restored JD Skills")
                            if "jd_skills" in doc and doc["jd_skills"]:
                                display_skill_tags(doc["jd_skills"], "neutral")
                            else:
                                st.caption("No skills stored.")
                        
                        st.divider()
                        st.text_area("Full Resume Text", doc.get('resume_text', ''), height=100, disabled=True, key=f"resume_text_{i}")
                        st.text_area("Full JD Text", doc.get('job_description', ''), height=100, disabled=True, key=f"jd_text_{i}")
                        
        else:
            st.info("No submissions found in your history.")

    elif page == "🚪 Logout":
        st.session_state.token = None
        st.session_state.user_email = None
        st.rerun()


import streamlit as st
from frontend.api_client import ingest_data, get_latest_ingestion

def show():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🚀 Data Ingestion Dashboard")
    st.info("Upload your documents to analyze skill matches and generate suggestions.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📄 Resume")
        resume_method = st.segmented_control("Input Method", ["Upload File", "Paste Text"], default="Upload File", key="resume_method")
        
        if resume_method == "Upload File":
            resume_file = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"], key="resume_file")
            if st.button("Process Resume", key="submit_resume_file", use_container_width=True):
                if resume_file:
                    with st.spinner("Analyzing resume..."):
                        result = ingest_data(st.session_state.token, "resume", file=resume_file)
                        if result["success"]:
                            st.success("Resume processed!")
                            st.toast("Resume uploaded successfully!", icon="✅")
                            st.rerun()
                        else:
                            st.error(f"Failed to upload resume: {result['error']}")
                else:
                    st.warning("Please select a file")
        else:
            resume_text = st.text_area("Paste Resume Content", height=250, key="resume_text", placeholder="Paste the text from your resume here...")
            if st.button("Analyze Resume Text", key="submit_resume_text", use_container_width=True):
                if resume_text:
                    with st.spinner("Analyzing text..."):
                        result = ingest_data(st.session_state.token, "resume", text=resume_text)
                        if result["success"]:
                            st.success("Resume text analyzed!")
                            st.toast("Resume text submitted!", icon="✅")
                            st.rerun()
                        else:
                            st.error(f"Failed to submit resume: {result['error']}")
                else:
                    st.warning("Please paste some text")
        
        # Show Latest Resume Preview
        latest_resume = get_latest_ingestion(st.session_state.token, "resume")
        if latest_resume.get("content"):
            with st.expander("🔍 View Current Resume Preview"):
                if latest_resume.get("filename"):
                    st.caption(f"Filename: {latest_resume['filename']}")
                st.text_area("Content", latest_resume["content"][:500] + "...", height=150, disabled=True, key="resume_preview")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 💼 Job Description")
        jd_method = st.segmented_control("Input Method", ["Upload File", "Paste Text"], default="Upload File", key="jd_method")
        
        if jd_method == "Upload File":
            jd_file = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"], key="jd_file")
            if st.button("Process Job Description", key="submit_jd_file", use_container_width=True):
                if jd_file:
                    with st.spinner("Analyzing JD..."):
                        result = ingest_data(st.session_state.token, "jd", file=jd_file)
                        if result["success"]:
                            st.success("JD processed!")
                            st.toast("Job description uploaded!", icon="✅")
                            st.rerun()
                        else:
                            st.error(f"Failed to upload JD: {result['error']}")
                else:
                    st.warning("Please select a file")
        else:
            jd_text = st.text_area("Paste JD Content", height=250, key="jd_text", placeholder="Paste the job description here...")
            if st.button("Analyze JD Text", key="submit_jd_text", use_container_width=True):
                if jd_text:
                    with st.spinner("Analyzing text..."):
                        result = ingest_data(st.session_state.token, "jd", text=jd_text)
                        if result["success"]:
                            st.success("JD text analyzed!")
                            st.toast("Job description submitted!", icon="✅")
                            st.rerun()
                        else:
                            st.error(f"Failed to submit JD: {result['error']}")
                else:
                    st.warning("Please paste some text")
        
        # Show Latest JD Preview
        latest_jd = get_latest_ingestion(st.session_state.token, "jd")
        if latest_jd.get("content"):
            with st.expander("🔍 View Current JD Preview"):
                if latest_jd.get("filename"):
                    st.caption(f"Filename: {latest_jd['filename']}")
                st.text_area("Content", latest_jd["content"][:500] + "...", height=150, disabled=True, key="jd_preview")
        st.markdown('</div>', unsafe_allow_html=True)

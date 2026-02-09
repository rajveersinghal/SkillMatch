import streamlit as st
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.pages import login, ingestion

st.set_page_config(page_title="SkillMatch - Milestone 1", layout="wide")

# Load custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css(os.path.join(os.path.dirname(__file__), "style.css"))

def main():
    if "token" not in st.session_state:
        st.session_state.token = None
    if "user_email" not in st.session_state:
        st.session_state.user_email = None

    st.markdown('<div class="ingestion-header"><h1 class="main-title">SkillMatch</h1></div>', unsafe_allow_html=True)
    
    st.sidebar.markdown("# 🚀 Navigation")
    
    try:
        if st.session_state.token:
            st.sidebar.markdown(f"### 👋 Welcome")
            st.sidebar.write(f"Logged in as: `{st.session_state.user_email}`")
            st.sidebar.markdown("### 🛠️ Menu")
            
            def feature_in_processing(name):
                st.toast(f"ℹ️ {name} is in processing...", icon="⏳")

            if st.sidebar.button("🚀 Dashboard", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()

            if st.sidebar.button("📄 My Resumes", use_container_width=True):
                feature_in_processing("My Resumes")
                
            if st.sidebar.button("💼 Job Descriptions", use_container_width=True):
                feature_in_processing("Job Descriptions")
                
            if st.sidebar.button("🕒 History", use_container_width=True):
                feature_in_processing("History")
            
            st.sidebar.markdown("---")
            if st.sidebar.button("🚪 Logout", use_container_width=True):
                st.session_state.token = None
                st.session_state.user_email = None
                st.toast("Logged out successfully!")
                st.rerun()
            
            st.sidebar.caption("v1.0.0 Stable")
            ingestion.show()
        else:
            login.show()
    except Exception as e:
        st.error(f"### ⚠️ An unexpected error occurred")
        st.exception(e)
        if st.button("Reset Application"):
            st.session_state.token = None
            st.rerun()

if __name__ == "__main__":
    main()

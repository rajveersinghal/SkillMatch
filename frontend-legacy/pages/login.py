import streamlit as st
from frontend.api_client import login_user, register_user

def show():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Create Account"])
        
        with tab1:
            st.markdown("### Welcome Back")
            email = st.text_input("Email", key="login_email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Log In", use_container_width=True):
                if not email or not password:
                    st.warning("Please enter both email and password")
                else:
                    with st.spinner("Authenticating..."):
                        result = login_user(email, password)
                        if result["success"]:
                            st.session_state.token = result["data"]["access_token"]
                            st.session_state.user_email = email
                            st.toast("Welcome back!", icon="👋")
                            st.rerun()
                        else:
                            st.error(result["error"])
                    
        with tab2:
            st.markdown("### Join SkillMatch")
            reg_email = st.text_input("Email", key="reg_email", placeholder="your@email.com")
            reg_password = st.text_input("Password", type="password", key="reg_pass", placeholder="Choose a strong password")
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Register Now", use_container_width=True):
                if not reg_email or not reg_password:
                    st.warning("Please enter both email and password")
                else:
                    with st.spinner("Creating account..."):
                        result = register_user(reg_email, reg_password)
                        if result["success"]:
                            st.success("Registration successful! You can now sign in.")
                            st.balloons()
                        else:
                            st.error(f"Registration failed: {result['error']}")
        st.markdown('</div>', unsafe_allow_html=True)

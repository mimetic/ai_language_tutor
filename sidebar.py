import streamlit as st

def render_sidebar():
    # --- Hide Default Sidebar Navigation ---
    st.markdown("""
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
        """, unsafe_allow_html=True)

    # --- Custom Sidebar Navigation ---
    st.sidebar.header("Navigation")
    
    # Vertical menu buttons
    if st.sidebar.button("Home", use_container_width=True, key="nav_home"):
        st.switch_page("app.py")
    
    if st.sidebar.button("Let's Talk", use_container_width=True, key="nav_chat"):
        st.switch_page("pages/chatbot.py")
    
    if st.sidebar.button("Vocabulary", use_container_width=True, key="nav_vocab"):
        st.switch_page("pages/vocab.py")
    
    if st.sidebar.button("Lesson Plan", use_container_width=True, key="nav_lesson"):
        st.switch_page("pages/lesson_plan.py")
    
    if st.sidebar.button("History", use_container_width=True, key="nav_history"):
        st.switch_page("pages/history.py")
    
    if st.sidebar.button("Settings", use_container_width=True, key="nav_settings"):
        st.switch_page("pages/settings.py")

import streamlit as st

def render_sidebar():
    # --- Hide Default Sidebar Navigation ---
    st.markdown("""
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        /* Sidebar button styling */
        .icon-button {
            display: inline-block;
            margin: 0 5px;
            text-align: center;
            font-size: 24px;
            width: 50px;
            height: 50px;
            line-height: 50px;
            border-radius: 50%;
            background-color: #f0f0f0;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .icon-button:hover {
            background-color: #e0e0e0;
        }
        /* Center icons horizontally */
        .icon-row {
            display: flex;
            justify-content: space-around;
            padding-top: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

    # --- Custom Sidebar ---
    # Icon Row for Navigation
    st.sidebar.markdown('<div class="icon-row">', unsafe_allow_html=True)

    col1, col2, col3, col4, col5, col6 = st.sidebar.columns(6)

    # Main Page Icon 🪐
    if col1.button("🪐", key="icon_app", help="Home"):
        st.switch_page("app.py")

    # Chatbot Icon 💬
    if col2.button("💬", key="icon_chatbot", help="Let's Talk"):
        st.switch_page("pages/chatbot.py")

    # Vocabulary Icon 📖
    if col3.button("📖", key="icon_vocab", help="Vocabulary"):
        st.switch_page("pages/vocab.py")

    # Lesson Plan Icon 📚
    if col4.button("📚", key="icon_lesson_plan", help="Lesson Plan"):
        st.switch_page("pages/lesson_plan.py")

    # History Icon 📜
    if col5.button("📜", key="icon_history", help="History"):
        st.switch_page("pages/history.py")
    
    # Settings Icon ⚙️
    if col6.button("⚙️", key="icon_settings", help="Settings"):
        st.switch_page("pages/settings.py")

    st.sidebar.markdown('</div>', unsafe_allow_html=True)

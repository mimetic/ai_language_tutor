import streamlit as st
from utils import storage

# --- Page Configuration ---
st.set_page_config(page_title="Language Learning Hub", page_icon="🪐", layout="wide")

# --- Load Lesson Plan ---
lesson_plan = storage.load_lesson_plan()  # Assuming lesson plan is stored as a list of dicts

# --- Calculate Progress ---
total_tasks = sum(len(week['assignments']) for week in lesson_plan)
completed_tasks = sum(
    1 for week in lesson_plan for task in week['assignments'] if task.get('completed', False)
)

progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0

# --- Render Sidebar (if you have it) ---
from sidebar import render_sidebar
render_sidebar()

# --- Main Page Content ---
st.title("🪐 Language Learning Hub")
st.write("Welcome to your personal AI-powered language tutor! Choose an activity.")

# Navigation Buttons in Main Content with Unique Keys
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("💬 Talk to your teaching assistant", key="main_chatbot"):
        st.switch_page("pages/chatbot.py")
with col2:
    if st.button("📖 Check out your vocabulary", key="main_vocab"):
        st.switch_page("pages/vocab.py")

with col3:
    if st.button("📚 Review your lessons plan", key="main_lesson_plan"):
        st.switch_page("pages/lesson_plan.py")
with col4:
    if st.button("📜 Look through the previous lessons", key="main_history"):
        st.switch_page("pages/history.py")


# --- Space-Themed Progress Bar ---
st.subheader("🚀 Your Learning Journey")

# Custom CSS for Space Road Progress Bar
st.markdown(f"""
    <style>
    .space-road {{
        position: relative;
        width: 100%;
        height: 60px;
        background: linear-gradient(to right, #a1c4fd, #c2e9fb);  /* Light blue gradient */
        border-radius: 30px;
        overflow: hidden;
        box-shadow: 0 0 15px rgba(0,0,0,0.2);
    }}
    .space-road::before {{
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        width: 100%;
        height: 4px;
        background: #ffffffb3;
        transform: translateY(-50%);
    }}
    .rocket {{
        position: absolute;
        top: 50%;
        left: {progress}%;
        width: 50px;
        height: 50px;
        background-image: url('https://www.iconpacks.net/icons/2/free-rocket-icon-3432-thumb.png');  /* Rocket icon */
        background-size: cover;
        transform: translate(-50%, -50%);
        transition: left 0.5s ease-in-out;
    }}
    .star {{
        position: absolute;
        width: 5px;
        height: 5px;
        background: #fff;
        border-radius: 50%;
        box-shadow: 0 0 10px #fff;
        animation: twinkle 2s infinite ease-in-out alternate;
    }}
    @keyframes twinkle {{
        from {{ opacity: 0.5; }}
        to {{ opacity: 1; }}
    }}
    </style>

    <div class="space-road">
        <div class="rocket"></div>
    </div>
    <p style="text-align: center; font-size: 18px;">{completed_tasks} out of {total_tasks} lessons completed ({progress:.2f}% 🚀)</p>
    """, unsafe_allow_html=True)

# Encouraging Messages
if progress == 0:
    st.info("🌌 Ready to start your journey? Your rocket is waiting for lift-off!")
elif progress < 50:
    st.success("🛸 You're cruising through the galaxy! Keep going!")
elif progress < 100:
    st.success("🚀 Almost there! The stars are within reach!")
else:
    st.balloons()
    st.success("🌟 Mission Accomplished! Well done, space explorer!")

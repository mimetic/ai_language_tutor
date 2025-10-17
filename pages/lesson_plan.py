# Version: 06.01
import streamlit as st
from utils import storage
from sidebar import render_sidebar
from utils.llm_client import chat_completion, get_llm_client, get_prompt
import json
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variables in Streamlit secrets
if "OPENAI_API_KEY" not in st.secrets and os.getenv("OPENAI_API_KEY"):
    st.secrets["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Lesson Plan", page_icon="📚", layout="wide")
render_sidebar()

# --- Load Configuration from config.json and environment ---
with open('utils/config.json', 'r') as config_file:
    config = json.load(config_file)

# Extract parameters from config
LANGUAGE = config.get('language', 'English')

# --- 🛠️ Initialize Lesson Plan and User Inputs in Session State ---
if "lesson_plan" not in st.session_state:
    st.session_state.lesson_plan = storage.load_lesson_plan()

if "lesson_plan_inputs" not in st.session_state:
    # Load saved inputs or initialize defaults
    saved_inputs = storage.load_lesson_plan_inputs()  # Implement this in storage
    st.session_state.lesson_plan_inputs = saved_inputs or {
        "user_level": "Beginner",
        "learning_period": "1 Month",
        "user_goals": ""
    }

# --- 📚 Lesson Plan Section ---
st.title("📚 Lesson Plan")
st.write("You can edit your plan by removing or adding items. Press 'Practice' to start lesson on the selected topic.")
st.write("Track your progress by crossing out the topics that you have already learned. Generate a new plan once your goals have changed.")


with st.sidebar:
    # Settings link
    if st.button("⚙️ Settings", help="Configure models and language settings"):
        st.switch_page("pages/settings.py")
    
    st.header("📚 Generate a Lesson Plan")

    # Pre-fill input fields with saved values
    user_level = st.selectbox(
        "Select your level:",
        ["Beginner", "Intermediate", "Advanced"],
        index=["Beginner", "Intermediate", "Advanced"].index(st.session_state.lesson_plan_inputs["user_level"])
    )

    learning_period = st.selectbox(
        "Study duration:",
        ["1 Week", "1 Month", "3 Months"],
        index=["1 Week", "1 Month", "3 Months"].index(st.session_state.lesson_plan_inputs["learning_period"])
    )

    user_goals = st.text_area(
        "Your learning goals:",
        value=st.session_state.lesson_plan_inputs["user_goals"]
    )

    if st.button("📜 Generate Lesson Plan"):
        # Save user inputs to session state and storage
        st.session_state.lesson_plan_inputs = {
            "user_level": user_level,
            "learning_period": learning_period,
            "user_goals": user_goals
        }
        storage.save_lesson_plan_inputs(st.session_state.lesson_plan_inputs)  # Implement in storage

        lesson_prompt = get_prompt('lesson_plan_generation', 
                                   level=user_level, 
                                   period=learning_period, 
                                   goals=user_goals)
        lesson_system = get_prompt('lesson_plan_system')

        with st.spinner("Generating lesson plan..."):
            response = chat_completion([
                {"role": "system", "content": lesson_system},
                {"role": "user", "content": lesson_prompt}
            ], model_type="lesson")

        # Extract JSON from response safely
        json_match = re.search(r'\{.*\}', response, re.DOTALL)

        if json_match:
            try:
                lesson_plan_json = json.loads(json_match.group())

                if "lesson_plan" in lesson_plan_json:
                    # Convert JSON into structured lesson format
                    formatted_plan = [
                        {"week_or_day": key, "assignments": [{"title": task, "completed": False} for task in value]}
                        for key, value in lesson_plan_json["lesson_plan"].items()
                    ]

                    # Save lesson plan
                    st.session_state.lesson_plan = formatted_plan
                    storage.save_lesson_plan(st.session_state.lesson_plan)
                    st.rerun()
                else:
                    st.error("Error: AI response did not include 'lesson_plan' key. Try again.")
            except json.JSONDecodeError:
                st.error("Error: AI response was not valid JSON. Try again.")
        else:
            st.error("Error: AI did not return JSON. Please try again.")

# --- 📝 Display and Manage Lesson Plan ---
if not st.session_state.lesson_plan:
    st.warning("No lesson plan available. Generate one from the sidebar!")
else:
    corrected_plan = []
    for entry in st.session_state.lesson_plan:
        if isinstance(entry, dict) and "week_or_day" in entry and "assignments" in entry:
            corrected_plan.append(entry)

    # Save corrected format
    if corrected_plan != st.session_state.lesson_plan:
        st.session_state.lesson_plan = corrected_plan
        storage.save_lesson_plan(st.session_state.lesson_plan)

    # Display lessons and assignments
    for i, lesson in enumerate(st.session_state.lesson_plan):
        st.markdown(f"### 🔹 {lesson['week_or_day']}")

        for j, assignment in enumerate(lesson["assignments"]):
            col1, col2, col3 = st.columns([0.7, 0.15, 0.15])

            # Task with completion checkbox
            with col1:
                completed = st.checkbox(
                    assignment["title"],
                    assignment["completed"],
                    key=f"lesson_{i}_assignment_{j}"
                )

                # Update completion status
                if completed != assignment["completed"]:
                    st.session_state.lesson_plan[i]["assignments"][j]["completed"] = completed
                    storage.save_lesson_plan(st.session_state.lesson_plan)

            # Play button to practice this item
            with col2:
                if st.button("▶️ Practice", key=f"play_{i}_{j}"):
                    # Set session state to send to chatbot
                    if "chatbot_preset" not in st.session_state or st.session_state.chatbot_preset is None:
                        st.session_state.chatbot_preset = f"Let's practice {assignment['title']}"
                        st.session_state.preset_locked = False  # Ensure it's processed only once
                    st.switch_page("pages/chatbot.py")  # Navigate to Chatbot

            # Delete button to remove task
            with col3:
                if st.button("❌", key=f"delete_{i}_{j}"):
                    del st.session_state.lesson_plan[i]["assignments"][j]
                    storage.save_lesson_plan(st.session_state.lesson_plan)
                    st.rerun()

        # Add a new assignment under each week/day
        new_task = st.text_input(f"➕ Add task for {lesson['week_or_day']}", key=f"new_task_{i}")
        if st.button(f"Add to {lesson['week_or_day']}", key=f"add_task_{i}"):
            if new_task.strip():
                st.session_state.lesson_plan[i]["assignments"].append({"title": new_task.strip(), "completed": False})
                storage.save_lesson_plan(st.session_state.lesson_plan)
                st.rerun()

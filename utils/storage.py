import json
import streamlit as st

VOCAB_FILE = "assets/user_vocabulary.json"
LESSON_PLAN_FILE = "assets/lesson_plan.json"
USER_INPUTS_FILE = "assets/lesson_plan_inputs.json"
CHAT_HISTORY_FILE = "assets/chat_history.json" # Define the file path for saving chat history

def save_lesson_plan_inputs(inputs):
    with open(USER_INPUTS_FILE, "w") as f:
        json.dump(inputs, f)

def load_lesson_plan_inputs():
    try:
        with open(USER_INPUTS_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

def load_vocabulary():
    try:
        with open(VOCAB_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_vocabulary(vocab_list):
    with open(VOCAB_FILE, "w") as f:
        json.dump(vocab_list, f)

def load_lesson_plan():
    try:
        with open(LESSON_PLAN_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_lesson_plan(plan):
    with open(LESSON_PLAN_FILE, "w") as f:
        json.dump(plan, f)

# --- Function to load chat history from file ---
def load_chat_history():
    try:
        with open(CHAT_HISTORY_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# --- Function to save chat history to file ---
def save_chat_history(messages):
    try:
        with open(CHAT_HISTORY_FILE, "w") as f:
            json.dump(messages, f)
    except Exception as e:
        st.error(f"Error saving chat history: {e}")

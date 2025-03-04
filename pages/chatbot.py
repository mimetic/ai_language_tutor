import streamlit as st
from utils import storage
from sidebar import render_sidebar
import openai
import random
import json

st.set_page_config(page_title="Let's talk", page_icon="💬", layout="wide")

# --- 💬 Chatbot Section ---
st.title("💬 Let's Talk")
st.write("Talk to your AI teaching assistant on any topic, ask for explanations of rules, useful vocabulary, or exercises.")
st.write("Save any new words to your vocabulary list in the side panel.")
st.write("Press 'Quiz!' to get exercises for practicing random words from your vocabulary list.")

# AI Response Function from the whole history
def get_ai_response_history(messages):
    client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=TEMPERATURE
    )
    return response.choices[0].message.content

# --- Initialize session state for messages if not present ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 📖 Vocabulary Panel ---
render_sidebar()
st.sidebar.header("💬 Your Teaching Assistant")

# --- Load Configuration from config.json ---
with open('utils/config.json', 'r') as config_file:
    config = json.load(config_file)

# Extract OpenAI model and temperature from config
OPENAI_MODEL = config.get('openai_model_name', 'gpt-4o')
TEMPERATURE = config.get('temperature', 0.7)

# Load vocabulary list
vocab_list = storage.load_vocabulary()

# Ensure all entries are dictionaries with 'word', 'translation', and 'example'
corrected_vocab_list = []
for entry in vocab_list:
    if isinstance(entry, str):
        corrected_vocab_list.append({
            "word": entry,
            "translation": "Brak.",
            "example": "Brak."
        })
    elif isinstance(entry, dict):
        corrected_vocab_list.append({
            "word": entry.get("word", "Unknown"),
            "translation": entry.get("translation", "Brak."),
            "example": entry.get("example", "Brak.")
        })

if corrected_vocab_list != vocab_list:
    storage.save_vocabulary(corrected_vocab_list)

vocab_list = corrected_vocab_list

# Display vocabulary in sidebar
if vocab_list:
    for word_entry in vocab_list:
        st.sidebar.markdown(f"- **{word_entry['word']}**")
else:
    st.sidebar.write("No words in your vocabulary.")

# --- 📋 Quiz Button ---
if st.sidebar.button("📝 Quiz!"):
    if len(vocab_list) < 1:
        st.sidebar.warning("Add at least one word to start a quiz.")
    else:
        quiz_words = random.sample(vocab_list, min(10, len(vocab_list)))
        quiz_word_list = [w["word"] for w in quiz_words]

        quiz_prompt = f"""
        You are a Polish language tutor. Create an engaging exercise using these words: {', '.join(quiz_word_list)}.
        Format it as a quiz that the user can answer.
        """

        with st.spinner("Generating quiz..."):
            quiz_response = get_ai_response_history([{"role": "user", "content": quiz_prompt}])

        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        st.session_state.messages.append({"role": "assistant", "content": quiz_response})
        
        with st.chat_message("assistant"):
            st.write(quiz_response)

# Chat interface
user_input = st.chat_input("Type your message...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    with st.spinner("Thinking..."):
        bot_reply = get_ai_response_history(st.session_state.messages)

    with st.chat_message("assistant"):
        st.write(bot_reply)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    
# Version: 04.15
import streamlit as st
from utils import storage
from sidebar import render_sidebar
from utils.llm_client import chat_completion, get_llm_client
from components.model_selector import render_model_selector
import random
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Let's talk", page_icon="💬", layout="wide")

# --- 💬 Chatbot Section ---
st.title("💬 Let's Talk")
st.write("Talk to your AI teaching assistant on any topic, ask for explanations of rules, useful vocabulary, or exercises.")
st.write("Save any new words to your vocabulary list in the side panel.")
st.write("Press 'Quiz!' to get exercises for practicing random words from your vocabulary list.")

# --- Load Configuration from config.json and environment ---
with open('utils/config.json', 'r') as config_file:
    config = json.load(config_file)

# Extract parameters from config and environment
LANGUAGE = config.get('language', 'English')

# Get LLM client info for display
try:
    llm_client = get_llm_client("chat")
    provider_info = llm_client.get_provider_info()
except Exception as e:
    st.error(f"Failed to initialize LLM client: {e}")
    st.stop()

# AI Response Function from the whole history
def get_ai_response_history(messages):
    return chat_completion(messages, model_type="chat")

# --- Initialize session state for messages if not present ---
if "messages" not in st.session_state:
    st.session_state.system_prompt = {"role": "system", "content": f"""
        You are a friendly personal {LANGUAGE} language tutor, helping to improve speaking skills. You:
        - Speak only in {LANGUAGE}, but provide translations if requested.
        - Plan lesson topics covering everyday situations, professional settings, and cultural aspects of {LANGUAGE} speaking countries.
        - Provide a list of key words and phrases for each topic, along with examples of usage.
        - Check user's answers to questions, correct mistakes, and explain grammar and pronunciation nuances. When correcting mistakes, you strike out incorrect words and write the correct ones in bold next to them, so the user can see errors. In the case of grammar mistakes, you remind the user of the relevant rule.
        - Keep the conversation going, ask guiding questions, engage the user in dialogues, and help them develop fluency.
        - Suggest more advanced vocabulary based on responses, ask follow-up questions, and encourage the user to use new words in context.
        - Maintain a vocabulary list of new words and occasionally remind the user to use them in conversation.
        - Recommend additional materials: movies, books, podcasts, and articles in {LANGUAGE}.
        - Encourage the user to think in {LANGUAGE} and not be afraid of mistakes, creating a friendly and motivating learning environment.
        """}

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 📖 Vocabulary Panel ---
render_sidebar()
st.sidebar.header("💬 Your Teaching Assistant")

# Model Selection Interface
render_model_selector()

# Load vocabulary list
vocab_list = storage.load_vocabulary()

# Ensure all entries are dictionaries with 'word', 'translation', and 'example'
corrected_vocab_list = []
for entry in vocab_list:
    if isinstance(entry, str):
        corrected_vocab_list.append({
            "word": entry,
            "translation": "None.",
            "example": "None."
        })
    elif isinstance(entry, dict):
        corrected_vocab_list.append({
            "word": entry.get("word", "Unknown"),
            "translation": entry.get("translation", "None."),
            "example": entry.get("example", "None.")
        })

if corrected_vocab_list != vocab_list:
    storage.save_vocabulary(corrected_vocab_list)

vocab_list = corrected_vocab_list

# Display vocabulary in sidebar

# --- Add New Word Section ---
new_word = st.sidebar.text_input("➕ Add a new word", key="new_vocab_word")

if st.sidebar.button("Add Word"):
    if new_word.strip() and all(w["word"] != new_word.strip() for w in vocab_list):
        prompt = f"""
        You are a {LANGUAGE} language expert. For the word "{new_word}", provide:
        1. A concise translation to English.
        2. One example sentence in {LANGUAGE} using the word.

        Format the response as:
        Translation: <your translation>
        Example: <your example>
        """

        with st.spinner(f"Fetching translation and example for '{new_word}'..."):
            response = chat_completion([{"role": "user", "content": prompt}], model_type="chat")

        # Parse the response
        content = response
        translation = ""
        example = ""

        for line in content.splitlines():
            if line.startswith("Translation:"):
                translation = line.replace("Translation:", "").strip()
            elif line.startswith("Example:"):
                example = line.replace("Example:", "").strip()

        if translation and example:
            # Add word with translation and example
            vocab_list.append({
                "word": new_word.strip(),
                "translation": translation,
                "example": example
            })
            storage.save_vocabulary(vocab_list)
            st.success(f"Added '{new_word}' with translation and example.")
            st.rerun()
        else:
            st.error("Failed to fetch translation and example. Try again.")
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
        You are a {LANGUAGE} language tutor. Create an engaging exercise using these words: {', '.join(quiz_word_list)}.
        Format it as a quiz that the user can answer.
        """

        with st.spinner("Generating quiz..."):
            quiz_response = get_ai_response_history(st.session_state.messages + [{"role": "user", "content": quiz_prompt}])

        st.session_state.messages.append({"role": "assistant", "content": quiz_response})
        
# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

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

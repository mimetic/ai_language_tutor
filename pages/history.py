import streamlit as st
import json
from datetime import datetime
from sidebar import render_sidebar
from utils import storage

st.set_page_config(page_title="Chat History", page_icon="📜")
st.title("📜 Chat History")
st.write("Look through your previous lessons.")
render_sidebar()
st.sidebar.header("📜 History of your lessons")

# --- Load messages from session state and save to file ---
if "messages" in st.session_state:
    # Filter out system prompts and add timestamps
    filtered_messages = [
        {**msg, "timestamp": msg.get("timestamp", datetime.now().isoformat())}
        for msg in st.session_state.messages
        if msg["role"] != "system"
    ]

    # Load existing history and append new messages
    existing_history = storage.load_chat_history()
    all_messages = existing_history + filtered_messages

    # Save updated chat history
    storage.save_chat_history(all_messages)

# --- Load saved chat history ---
chat_history = storage.load_chat_history()

# --- Group messages by date ---
history_by_date = {}
for msg in chat_history:
    msg_time = datetime.fromisoformat(msg["timestamp"])
    date_str = msg_time.strftime("%Y-%m-%d")

    if date_str not in history_by_date:
        history_by_date[date_str] = []
    history_by_date[date_str].append(msg)

# --- Display grouped history ---
if not history_by_date:
    st.warning("No conversation history available.")
else:
    for date, messages in sorted(history_by_date.items(), reverse=True):
        with st.expander(f"📅 {date}"):
            for msg in messages:
                role = "👤 User" if msg["role"] == "user" else "🤖 Chatbot"
                st.markdown(f"**{role}:** {msg['content']}")

import streamlit as st
import json
from datetime import datetime
from sidebar import render_sidebar
from utils import storage

st.set_page_config(page_title="Lesson History", page_icon="📜")
st.title("📜 Lesson History")
st.write("Look through your previous lessons.")
render_sidebar()
st.sidebar.header("📜 History of your lessons")

# --- Load messages from session state and ensure timestamps ---
if "messages" in st.session_state:
    new_messages = []
    for msg in st.session_state.messages:
        if msg["role"] != "system":  # Exclude system messages
            if "timestamp" not in msg:  # Ensure timestamp exists
                msg["timestamp"] = datetime.now().isoformat()
            new_messages.append(msg)

    # Load existing chat history
    existing_history = storage.load_chat_history()

    # Append only new messages
    unique_messages = {m["timestamp"]: m for m in existing_history}  # Use timestamp as unique key
    for msg in new_messages:
        unique_messages[msg["timestamp"]] = msg  # Avoid overwriting existing ones

    # Save updated chat history
    updated_chat_history = list(unique_messages.values())
    existing_history = storage.load_chat_history()
    storage.save_chat_history(existing_history + new_messages)


# --- Load saved chat history ---
chat_history = storage.load_chat_history()

# --- Group messages by date ---
history_by_date = {}
invalid_timestamps = []

for msg in chat_history:
    try:
        msg_time = datetime.strptime(msg["timestamp"][:19], "%Y-%m-%dT%H:%M:%S")
     # Convert timestamp
        date_str = msg_time.strftime("%Y-%m-%d")  # Extract date part only

        if date_str not in history_by_date:
            history_by_date[date_str] = []
        history_by_date[date_str].append(msg)

    except ValueError as e:
        invalid_timestamps.append(msg["timestamp"])  # Store problematic timestamps



# --- Display grouped history ---
if not history_by_date:
    st.warning("No conversation history available.")
else:
    for date, messages in sorted(history_by_date.items(), reverse=True):
        with st.expander(f"📅 {date}"):
            for msg in messages:
                role = "👤 User" if msg["role"] == "user" else "🤖 Chatbot"
                st.markdown(f"**{role}:** {msg['content']}")

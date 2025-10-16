# Version: 01.01
import streamlit as st
from utils.llm_client import get_llm_client, get_available_models, set_model_for_type, load_config

def render_model_selector():
    """Render model selection interface in sidebar"""
    
    st.sidebar.header("🤖 Model Selection")
    
    # Load current configuration
    config = load_config()
    llm_models = config.get("llm_models", {"chat": None, "lesson": None, "available": []})
    
    # Get available models (use cached if available)
    available_models = llm_models.get("available", [])
    
    # Refresh models button
    col1, col2 = st.sidebar.columns([3, 1])
    with col2:
        if st.button("🔄", help="Refresh available models"):
            client = get_llm_client()
            available_models = client.refresh_available_models()
            st.rerun()
    
    with col1:
        st.write("**Available Models:**")
    
    if not available_models:
        st.sidebar.warning("No models available. Check your provider connection.")
        # Try to refresh automatically
        try:
            client = get_llm_client()
            available_models = client.refresh_available_models()
        except Exception:
            pass
    
    if available_models:
        # Model selection for chat
        st.sidebar.subheader("💬 Chat Model")
        current_chat_model = llm_models.get("chat") or get_llm_client("chat").model
        
        model_options = [f"{model['name']} ({model['id']})" for model in available_models]
        model_ids = [model['id'] for model in available_models]
        
        # Find current selection index
        try:
            current_chat_idx = model_ids.index(current_chat_model) if current_chat_model in model_ids else 0
        except ValueError:
            current_chat_idx = 0
        
        selected_chat_idx = st.sidebar.selectbox(
            "Select model for chat:",
            range(len(model_options)),
            format_func=lambda x: model_options[x],
            index=current_chat_idx,
            key="chat_model_selector"
        )
        
        selected_chat_model = model_ids[selected_chat_idx]
        
        if selected_chat_model != current_chat_model:
            set_model_for_type("chat", selected_chat_model)
            st.sidebar.success(f"Chat model updated to {available_models[selected_chat_idx]['name']}")
            st.rerun()
        
        # Model selection for lesson/quiz
        st.sidebar.subheader("📚 Lesson/Quiz Model")
        current_lesson_model = llm_models.get("lesson") or get_llm_client("lesson").model
        
        # Find current selection index
        try:
            current_lesson_idx = model_ids.index(current_lesson_model) if current_lesson_model in model_ids else 0
        except ValueError:
            current_lesson_idx = 0
        
        selected_lesson_idx = st.sidebar.selectbox(
            "Select model for lessons/quizzes:",
            range(len(model_options)),
            format_func=lambda x: model_options[x],
            index=current_lesson_idx,
            key="lesson_model_selector"
        )
        
        selected_lesson_model = model_ids[selected_lesson_idx]
        
        if selected_lesson_model != current_lesson_model:
            set_model_for_type("lesson", selected_lesson_model)
            st.sidebar.success(f"Lesson model updated to {available_models[selected_lesson_idx]['name']}")
            st.rerun()
        
        # Current model info
        with st.sidebar.expander("📊 Current Models", expanded=False):
            chat_client = get_llm_client("chat")
            lesson_client = get_llm_client("lesson")
            
            st.write(f"**Chat:** {chat_client.model}")
            st.write(f"**Lesson:** {lesson_client.model}")
            st.write(f"**Provider:** {chat_client.provider.upper()}")
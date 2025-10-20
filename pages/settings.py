# Version: 07.01
import streamlit as st
from utils.llm_client import get_llm_client, get_available_models, set_model_for_type, load_config, save_config, set_model_settings
from utils.llm_client import get_prompt
import json

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")

st.title("⚙️ Settings")
st.write("Configure your AI Language Tutor settings")

# Load current configuration
config = load_config()

# Create tabs for different settings categories
tab1, tab2, tab3 = st.tabs(["🤖 Model Selection", "🌍 Language & Prompts", "ℹ️ System Info"])

with tab1:
    st.header("🤖 LLM Model Configuration")
    
    # Load current configuration
    llm_models = config.get("llm_models", {"chat": None, "lesson": None, "available": []})
    
    # Provider information
    try:
        chat_client = get_llm_client("chat")
        provider_info = chat_client.get_provider_info()
        
        st.subheader("Current Provider")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.info(f"**Provider:** {provider_info['provider'].upper()}")
            if provider_info.get('base_url'):
                st.info(f"**Base URL:** {provider_info['base_url']}")
        
        with col2:
            if st.button("🔄 Refresh Models", help="Refresh available models from provider"):
                with st.spinner("Refreshing models..."):
                    available_models = chat_client.refresh_available_models()
                    st.success(f"Found {len(available_models)} models")
                    st.rerun()
    
    except Exception as e:
        st.error(f"Failed to connect to LLM provider: {e}")
        st.stop()
    
    # Get available models
    available_models = llm_models.get("available", [])
    
    if not available_models:
        st.warning("No models available. Please refresh models or check your provider connection.")
        if st.button("🔄 Try Refresh Now"):
            try:
                client = get_llm_client()
                available_models = client.refresh_available_models()
                st.rerun()
            except Exception as e:
                st.error(f"Failed to refresh models: {e}")
    
    if available_models:
        st.subheader("Model Selection")
        
        # Filter out embedding models for cleaner interface
        text_models = [m for m in available_models if 'embedding' not in m['id'].lower() and 'whisper' not in m['id'].lower()]
        
        if not text_models:
            text_models = available_models  # Fallback to all models if no text models found
        
        model_options = [f"{model['name']}" for model in text_models]
        model_ids = [model['id'] for model in text_models]
        
        # Chat Model Selection
        st.markdown("### 💬 Chat Model")
        st.write("Model used for conversations, vocabulary translation, and quizzes")
        
        current_chat_model = llm_models.get("chat") or get_llm_client("chat").model
        
        try:
            current_chat_idx = model_ids.index(current_chat_model) if current_chat_model in model_ids else 0
        except ValueError:
            current_chat_idx = 0
        
        selected_chat_idx = st.selectbox(
            "Select chat model:",
            range(len(model_options)),
            format_func=lambda x: model_options[x],
            index=current_chat_idx,
            key="settings_chat_model_selector"
        )
        
        selected_chat_model = model_ids[selected_chat_idx]
        
        if st.button("💬 Update Chat Model", key="update_chat"):
            if selected_chat_model != current_chat_model:
                set_model_for_type("chat", selected_chat_model)
                st.success(f"✅ Chat model updated to: **{text_models[selected_chat_idx]['name']}**")
                st.rerun()
            else:
                st.info("Chat model is already set to the selected model")
        
        # Chat model settings
        chat_settings = config.get("llm_models", {}).get("chat_settings", {"temperature": 0.1, "max_tokens": 1000})
        
        col1, col2 = st.columns(2)
        with col1:
            chat_temp = st.slider(
                "Temperature:",
                min_value=0.0,
                max_value=2.0,
                value=float(chat_settings.get("temperature", 0.1)),
                step=0.1,
                key="chat_temperature",
                help="Controls randomness. Lower = more focused, Higher = more creative"
            )
        
        with col2:
            chat_tokens = st.number_input(
                "Max Tokens:",
                min_value=100,
                max_value=4000,
                value=int(chat_settings.get("max_tokens", 1000)),
                step=100,
                key="chat_max_tokens",
                help="Maximum response length"
            )
        
        if st.button("⚙️ Update Chat Settings", key="update_chat_settings"):
            set_model_settings("chat", chat_temp, chat_tokens)
            st.success("✅ Chat model settings updated!")
            st.rerun()
        
        st.divider()
        
        # Lesson/Quiz Model Selection  
        st.markdown("### 📚 Lesson/Quiz Model")
        st.write("Model used for generating lesson plans and structured content")
        
        current_lesson_model = llm_models.get("lesson") or get_llm_client("lesson").model
        
        try:
            current_lesson_idx = model_ids.index(current_lesson_model) if current_lesson_model in model_ids else 0
        except ValueError:
            current_lesson_idx = 0
        
        selected_lesson_idx = st.selectbox(
            "Select lesson/quiz model:",
            range(len(model_options)),
            format_func=lambda x: model_options[x],
            index=current_lesson_idx,
            key="settings_lesson_model_selector"
        )
        
        selected_lesson_model = model_ids[selected_lesson_idx]
        
        if st.button("📚 Update Lesson Model", key="update_lesson"):
            if selected_lesson_model != current_lesson_model:
                set_model_for_type("lesson", selected_lesson_model)
                st.success(f"✅ Lesson model updated to: **{text_models[selected_lesson_idx]['name']}**")
                st.rerun()
            else:
                st.info("Lesson model is already set to the selected model")
        
        # Lesson model settings
        lesson_settings = config.get("llm_models", {}).get("lesson_settings", {"temperature": 0.1, "max_tokens": 1500})
        
        col1, col2 = st.columns(2)
        with col1:
            lesson_temp = st.slider(
                "Temperature:",
                min_value=0.0,
                max_value=2.0,
                value=float(lesson_settings.get("temperature", 0.1)),
                step=0.1,
                key="lesson_temperature",
                help="Controls randomness. Lower = more focused, Higher = more creative"
            )
        
        with col2:
            lesson_tokens = st.number_input(
                "Max Tokens:",
                min_value=100,
                max_value=4000,
                value=int(lesson_settings.get("max_tokens", 1500)),
                step=100,
                key="lesson_max_tokens",
                help="Maximum response length"
            )
        
        if st.button("⚙️ Update Lesson Settings", key="update_lesson_settings"):
            set_model_settings("lesson", lesson_temp, lesson_tokens)
            st.success("✅ Lesson model settings updated!")
            st.rerun()
        
        # Quick Actions
        st.divider()
        st.subheader("Quick Actions")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Use Same Model for Both", help="Set both chat and lesson to use the same model"):
                if selected_chat_model != current_lesson_model:
                    set_model_for_type("lesson", selected_chat_model)
                    st.success(f"Both models set to: {text_models[selected_chat_idx]['name']}")
                    st.rerun()
        
        with col2:
            best_model = text_models[0] if text_models else None
            if best_model and st.button("⭐ Use Best Model", help="Set both to the first available model"):
                set_model_for_type("chat", best_model['id'])
                set_model_for_type("lesson", best_model['id'])
                st.success(f"Both models set to: {best_model['name']}")
                st.rerun()
        
        with col3:
            if st.button("ℹ️ Model Details", help="Show detailed information about selected models"):
                st.session_state.show_model_details = not st.session_state.get("show_model_details", False)
                st.rerun()
        
        # Model Details (collapsible)
        if st.session_state.get("show_model_details", False):
            st.subheader("📊 Current Model Configuration")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**💬 Chat Model**")
                chat_client = get_llm_client("chat")
                st.code(f"""Model: {chat_client.model}
Provider: {chat_client.provider}
Temperature: {chat_client.temperature}
Max Tokens: {chat_client.max_tokens}""")
            
            with col2:
                st.markdown("**📚 Lesson Model**") 
                lesson_client = get_llm_client("lesson")
                st.code(f"""Model: {lesson_client.model}
Provider: {lesson_client.provider}
Temperature: {lesson_client.temperature}
Max Tokens: {lesson_client.max_tokens}""")

with tab2:
    st.header("🌍 Language & Learning Configuration")
    
    # Language selection
    current_language = config.get('language', 'German')
    
    languages = [
        "German", "Spanish", "French", "Italian", "Portuguese", 
        "Dutch", "Russian", "Japanese", "Chinese", "Korean",
        "Arabic", "Hindi", "Swedish", "Norwegian", "Danish"
    ]
    
    selected_language = st.selectbox(
        "Learning Language:",
        languages,
        index=languages.index(current_language) if current_language in languages else 0
    )
    
    if st.button("🌍 Update Language"):
        if selected_language != current_language:
            config['language'] = selected_language
            save_config(config)
            st.success(f"✅ Learning language updated to: **{selected_language}**")
            st.info("Please refresh the app to see changes in prompts")
            st.rerun()
        else:
            st.info("Language is already set to the selected language")
    
    st.divider()
    
    # Prompt customization info
    st.subheader("🎯 Prompt Customization")
    st.write("Edit AI prompts to customize behavior:")
    
    available_prompts = list(config.get('prompts', {}).keys())
    if available_prompts:
        selected_prompt = st.selectbox(
            "Select prompt to edit:",
            available_prompts,
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        if selected_prompt:
            current_prompt = config.get('prompts', {}).get(selected_prompt, '')
            
            # Edit prompt in text area with word wrap
            edited_prompt = st.text_area(
                f"Edit {selected_prompt.replace('_', ' ').title()}:",
                value=current_prompt,
                height=200,
                help="Variables: {language}, {word}, {words}, {level}, {period}, {goals}",
                key=f"edit_{selected_prompt}"
            )
            
            # Show preview of formatted prompt
            if edited_prompt != current_prompt:
                st.subheader("Preview (with sample variables):")
                try:
                    preview = edited_prompt.format(
                        language=config.get('language', 'German'),
                        word="example",
                        words="word1, word2", 
                        level="A1",
                        period="1 Month",
                        goals="Learn basics"
                    )
                    st.text_area("Preview:", preview, height=150, disabled=True)
                except Exception as e:
                    st.warning(f"Preview error: {e}")
            
            # Save button
            if st.button(f"💾 Save {selected_prompt.replace('_', ' ').title()}", key=f"save_{selected_prompt}"):
                if edited_prompt != current_prompt:
                    config['prompts'][selected_prompt] = edited_prompt
                    save_config(config)
                    st.success(f"✅ {selected_prompt.replace('_', ' ').title()} prompt saved!")
                    st.rerun()
                else:
                    st.info("No changes to save")

with tab3:
    st.header("ℹ️ System Information")
    
    # Configuration overview
    st.subheader("📋 Current Configuration")
    
    config_display = {
        "Language": config.get('language', 'Not set'),
        "Chat Model": config.get('llm_models', {}).get('chat', 'Not set'),
        "Lesson Model": config.get('llm_models', {}).get('lesson', 'Not set'),
        "Available Models": len(config.get('llm_models', {}).get('available', [])),
        "Prompts Configured": len(config.get('prompts', {}))
    }
    
    for key, value in config_display.items():
        st.write(f"**{key}:** {value}")
    
    st.divider()
    
    # Advanced options
    st.subheader("🔧 Advanced Options")
    
    if st.button("📄 View Full Configuration", help="Show complete config.json content"):
        st.json(config)
    
    if st.button("🔄 Reset Model Cache", help="Clear cached model list and refresh"):
        try:
            config['llm_models']['available'] = []
            save_config(config)
            st.success("Model cache cleared. Refresh models on the Model Selection tab.")
        except Exception as e:
            st.error(f"Failed to reset cache: {e}")
    
    st.divider()
    
    # Help information
    st.subheader("❓ Help & Documentation")
    st.markdown("""
    **Model Selection:**
    - Chat models handle conversations and vocabulary translation
    - Lesson models generate structured learning content
    - You can use the same model for both functions
    
    **Configuration Files:**
    - `utils/config.json` - Main configuration and prompts
    - `.env` - Environment variables and API keys
    - `PROMPT_CUSTOMIZATION.md` - Prompt customization guide
    
    **Troubleshooting:**
    - If models don't appear, check your provider connection
    - Restart the app after changing language settings
    - Check console for detailed error messages
    """)


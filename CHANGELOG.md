# Changelog

All notable changes to the AI Language Tutor project will be documented in this file.

## [06.01] - 2025-10-17

### 🎯 Major Features Added
- **Centralized Settings Page**: New dedicated Settings page (`pages/settings.py`) with organized tabs for configuration
- **Enhanced Model Selection**: Improved model selection interface moved from sidebar to Settings page
- **Multi-Language Support**: Easy language switching with 15+ supported languages
- **Prompt Configuration Management**: All AI prompts moved to `config.json` for easy customization
- **System Diagnostics**: Advanced system information and troubleshooting tools

### 🔧 Configuration Management
- **Config-Based Prompts**: All AI prompts now stored in `utils/config.json` instead of hardcoded in Python files
- **Prompt Variable Substitution**: Dynamic prompt generation with `{language}`, `{word}`, etc. variables
- **Model Precedence**: Config settings now properly override environment variables
- **Centralized Language Settings**: Language configuration moved to Settings page

### 🎨 User Interface Improvements
- **Clean Sidebar Navigation**: Removed bulky model selectors from sidebars
- **Settings Icon**: Added ⚙️ Settings icon to main navigation and all pages
- **Organized Tabs**: Settings organized into Model Selection, Language & Prompts, and System Info tabs
- **Better Model Filtering**: Automatically filters embedding/whisper models for cleaner interface
- **Quick Actions**: One-click buttons for common model configuration tasks

### 🐛 Bug Fixes
- **System Prompt Integration**: Fixed issue where chatbot wasn't receiving system prompts from config
- **Message Structure**: Corrected LLM message structure to include system prompt in conversations
- **Model Type Handling**: Improved model type selection for chat vs lesson generation

### 📚 Technical Improvements
- **Enhanced LLM Client**: Added prompt loading, model discovery, and configuration management
- **Type Safety**: Added proper type hints and error handling
- **Code Organization**: Better separation of concerns with dedicated settings functionality
- **Deprecation Management**: Properly deprecated old model selector component

### 📖 Documentation Updates
- **Updated README**: Comprehensive documentation of new Settings page and features
- **Prompt Customization Guide**: Detailed guide for customizing AI prompts
- **Configuration Examples**: Clear examples for different use cases
- **Troubleshooting Guide**: Enhanced troubleshooting information

### 🔄 Migration Notes
- **Model Selection**: Model selection has moved from sidebar to Settings page (⚙️ icon)
- **Prompt Customization**: Prompts can now be customized in `utils/config.json`
- **Language Settings**: Language configuration available in Settings page
- **Navigation**: Settings accessible from main navigation bar and all pages

### 📦 Files Added
- `pages/settings.py` - New comprehensive settings page
- `CHANGELOG.md` - This changelog file
- `PROMPT_CUSTOMIZATION.md` - Prompt customization documentation

### 📦 Files Modified
- `utils/llm_client.py` - Enhanced with prompt loading and model management
- `utils/config.json` - Added prompts section and enhanced model configuration
- `pages/chatbot.py` - System prompt integration and settings navigation
- `pages/lesson_plan.py` - Settings navigation and config-based prompts
- `pages/vocab.py` - Settings navigation and config-based prompts
- `app.py` - Added Settings button to main navigation
- `sidebar.py` - Added Settings icon to navigation bar
- `.env.example` - Updated with new model selection environment variables
- `README.md` - Comprehensive documentation updates

### 📦 Files Deprecated
- `components/model_selector.py` - Deprecated in favor of Settings page

---

## [05.02] - Previous Version
- Fixed system prompt integration in chatbot
- Improved message structure for LLM calls

## [05.01] - Previous Version  
- Added model selection functionality
- Implemented LM Studio model discovery
- Created config-based model management
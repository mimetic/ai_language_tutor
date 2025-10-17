# Version 06.01: Major Settings & Configuration Update

## 🎯 Major Features
- **NEW**: Centralized Settings page with organized tabs (Model Selection, Language & Prompts, System Info)
- **NEW**: Multi-language support with easy switching (15+ languages)
- **NEW**: Config-based prompt management with variable substitution
- **NEW**: Advanced system diagnostics and troubleshooting tools

## 🔧 Configuration Management
- **MOVED**: All AI prompts from code to `utils/config.json` for easy customization
- **ADDED**: Dynamic prompt generation with `{language}`, `{word}`, etc. variables
- **IMPROVED**: Config settings now properly override environment variables
- **ENHANCED**: Model selection with better filtering and quick actions

## 🎨 User Interface
- **RELOCATED**: Model selection moved from sidebar to dedicated Settings page (⚙️)
- **ADDED**: Settings icon to main navigation and all pages
- **CLEANED**: Removed bulky model selectors from sidebars
- **ORGANIZED**: Settings grouped in logical tabs with helpful descriptions

## 🐛 Bug Fixes
- **FIXED**: System prompt integration - chatbot now properly receives system prompts
- **CORRECTED**: LLM message structure to include system prompt in all conversations
- **IMPROVED**: Model type handling for chat vs lesson generation

## 📖 Documentation
- **UPDATED**: README with comprehensive Settings page documentation
- **ADDED**: PROMPT_CUSTOMIZATION.md guide for customizing AI prompts
- **CREATED**: CHANGELOG.md for tracking version changes
- **ENHANCED**: Configuration examples and troubleshooting guide

## 🔄 Breaking Changes
- Model selection has moved from sidebar to Settings page
- Prompts are now in config.json (automatic migration)
- Settings accessible via ⚙️ icon instead of sidebar

## 📦 Files Added
- `pages/settings.py` - Comprehensive settings page
- `CHANGELOG.md` - Version change tracking
- `PROMPT_CUSTOMIZATION.md` - Prompt customization guide
- `VERSION` - Current version tracking

---
Ready for production deployment with enhanced user experience and maintainability.
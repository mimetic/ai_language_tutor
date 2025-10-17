# Prompt Customization Guide

This document explains how to customize the AI prompts used throughout the Language Tutor application.

## Overview

All prompts are now stored in `utils/config.json` under the `prompts` section. This makes it easy to:
- Customize AI behavior without changing code
- Create different teaching styles 
- Add support for new languages
- Experiment with different prompt strategies

## Available Prompts

### 1. `chatbot_system`
The main system prompt for the chatbot tutor.

**Variables:** `{language}`

**Default behavior:** Friendly language tutor that provides corrections, examples, and cultural context.

### 2. `word_translation`  
Prompt for translating individual words with examples.

**Variables:** `{language}`, `{word}`

**Purpose:** Generates translation and usage example for vocabulary words.

### 3. `word_translation_system`
System prompt for word translation requests.

**Variables:** `{language}`

**Purpose:** Sets the context for translation tasks.

### 4. `quiz_generation`
Prompt for creating vocabulary quizzes.

**Variables:** `{language}`, `{words}`

**Purpose:** Creates engaging exercises using the user's vocabulary list.

### 5. `lesson_plan_generation`
Prompt for generating structured lesson plans.

**Variables:** `{language}`, `{level}`, `{period}`, `{goals}`

**Purpose:** Creates personalized learning curricula in JSON format.

### 6. `lesson_plan_system`
System prompt for lesson plan generation.

**Variables:** None

**Purpose:** Ensures consistent JSON output format for lesson plans.

## Customization Examples

### Making the Tutor More Formal

Edit the `chatbot_system` prompt:
```json
"chatbot_system": "You are a professional {language} language instructor. You provide structured lessons with formal grammar explanations..."
```

### Adding Cultural Focus

```json
"chatbot_system": "You are a {language} language and culture expert. Emphasize cultural context, traditions, and social norms when teaching {language}..."
```

### Specialized Vocabulary Training

```json
"word_translation": "You are a {language} specialist in [DOMAIN]. For the word \"{word}\", provide:\n1. Professional translation\n2. Technical usage example\n3. Industry context"
```

## Variable Substitution

The system automatically substitutes these variables:
- `{language}` - The learning language from config
- `{word}` - Specific vocabulary word
- `{words}` - List of words for quizzes  
- `{level}` - User's proficiency level
- `{period}` - Learning timeframe
- `{goals}` - User's learning objectives

## Best Practices

1. **Test Changes:** Always test prompt modifications with real conversations
2. **Keep Backups:** Save working prompts before major changes
3. **Use Clear Instructions:** Be specific about expected output format
4. **Consider Context:** Remember these prompts work together as a system
5. **Language Support:** Use `{language}` variable for multi-language support

## Troubleshooting

- **Variable Errors:** Ensure all `{variable}` placeholders have corresponding values
- **Format Issues:** Check JSON syntax if the config file won't load
- **Behavior Changes:** Restart the Streamlit app after prompt modifications

## Advanced Usage

For advanced users, you can:
- Add new prompt types by modifying `utils/llm_client.py`
- Create prompt variations for different user levels
- Implement A/B testing with multiple prompt versions
- Add conditional logic based on user progress
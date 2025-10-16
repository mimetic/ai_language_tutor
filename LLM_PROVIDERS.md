# Version: 01.00
# LLM Provider Configuration Guide

This AI Language Tutor supports three different LLM providers:

## Supported Providers

### 1. OpenAI
- **Provider code**: `openai`
- **Models**: `gpt-3.5-turbo`, `gpt-4`, `gpt-4o`, etc.
- **Requirements**: Valid OpenAI API key

### 2. LM Studio (Local)
- **Provider code**: `lmstudio`
- **Models**: Any model loaded in LM Studio
- **Requirements**: LM Studio running locally with local server enabled

### 3. Ollama (Local)
- **Provider code**: `ollama`
- **Models**: Any model installed in Ollama (e.g., `llama2`, `mistral`, `qwen2.5-7b-instruct`)
- **Requirements**: Ollama running locally

## Configuration

### Environment Variables (.env file)

```bash
# LLM Provider Configuration
LLM_PROVIDER=lmstudio                    # Options: openai, lmstudio, ollama
LLM_MODEL=qwen2.5-7b-instruct           # Model name specific to your provider
LLM_TEMPERATURE=0.1                     # Temperature for responses (0.0-2.0)
LLM_MAX_TOKENS=1000                     # Maximum tokens for responses

# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY=your-openai-api-key-here

# LM Studio Configuration (if using LM Studio)
LMSTUDIO_BASE_URL=http://localhost:1234/v1

# Ollama Configuration (if using Ollama)
OLLAMA_BASE_URL=http://localhost:11434
```

## Setup Instructions

### For OpenAI
1. Set `LLM_PROVIDER=openai`
2. Set your `OPENAI_API_KEY`
3. Choose your model (e.g., `LLM_MODEL=gpt-4o`)

### For LM Studio
1. Download and install [LM Studio](https://lmstudio.ai/)
2. Load a model in LM Studio
3. Start the local server (usually on port 1234)
4. Set `LLM_PROVIDER=lmstudio`
5. Set `LLM_MODEL` to the exact model name shown in LM Studio
6. Set `LMSTUDIO_BASE_URL=http://localhost:1234/v1`

### For Ollama
1. Install [Ollama](https://ollama.ai/)
2. Pull a model: `ollama pull qwen2.5-7b-instruct`
3. Ensure Ollama is running: `ollama serve`
4. Set `LLM_PROVIDER=ollama`
5. Set `LLM_MODEL` to your installed model name
6. Set `OLLAMA_BASE_URL=http://localhost:11434`

## Model Recommendations

### For Learning Languages
- **OpenAI**: `gpt-4o` or `gpt-4` for best quality
- **Local options**: 
  - `qwen2.5-7b-instruct` - Good multilingual support
  - `mistral-7b-instruct` - Good general performance
  - `llama3-8b-instruct` - Solid all-around model

### Performance Considerations
- **OpenAI**: Fastest responses, requires internet and API costs
- **LM Studio**: Good performance with proper hardware (8GB+ VRAM recommended)
- **Ollama**: Easy setup, moderate performance depending on model size

## Troubleshooting

### Common Issues
1. **Connection errors**: Ensure local servers are running on correct ports
2. **Model not found**: Verify model names match exactly what's installed
3. **Slow responses**: Consider using smaller models for local setups
4. **Memory issues**: Use quantized models (Q4 or Q8) for local setups

### Checking Configuration
The chatbot page shows your current LLM provider configuration in the sidebar under "🤖 LLM Provider Info".

## Switching Providers
Simply update the `.env` file and restart the Streamlit application:
```bash
streamlit run app.py
```

The application will automatically use the new provider configuration.
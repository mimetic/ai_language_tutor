# Version: 04.15
import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from typing import List, Dict, Optional

# Load environment variables
load_dotenv()

# Set environment variables in Streamlit secrets for compatibility
if "OPENAI_API_KEY" not in st.secrets and os.getenv("OPENAI_API_KEY"):
    st.secrets["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def load_config():
    """Load configuration from config.json"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"language": "English", "llm_models": {"chat": None, "lesson": None, "available": []}}

def save_config(config):
    """Save configuration to config.json"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

class LLMClient:
    """Unified LLM client supporting OpenAI, LM Studio, and Ollama with model selection"""
    
    def __init__(self, model_type: str = "chat"):
        self.provider = os.getenv("LLM_PROVIDER", "openai").lower()
        self.model_type = model_type
        self.temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("LLM_MAX_TOKENS", "1000"))
        
        # Load config for model selection
        self.config = load_config()
        
        # Determine model to use (config overrides env)
        self.model = self._get_model_for_type(model_type)
        
        # Initialize provider-specific settings
        if self.provider == "openai":
            self.api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY in .env file or Streamlit secrets.")
            self.client = OpenAI(api_key=self.api_key)
        
        elif self.provider == "lmstudio":
            self.base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
            self.client = OpenAI(
                base_url=self.base_url,
                api_key="lm-studio"  # LM Studio uses a dummy key
            )
        
        elif self.provider == "ollama":
            self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")
    
    def _get_model_for_type(self, model_type: str) -> str:
        """Get the appropriate model for the given type (chat/lesson)"""
        # Check config first
        config_model = self.config.get("llm_models", {}).get(model_type)
        if config_model:
            return config_model
        
        # Fall back to env variables
        if model_type == "chat":
            return os.getenv("LLM_MODEL_CHAT") or os.getenv("LLM_MODEL", "gpt-4o")
        elif model_type == "lesson":
            return os.getenv("LLM_MODEL_LESSON") or os.getenv("LLM_MODEL", "gpt-4o")
        else:
            return os.getenv("LLM_MODEL", "gpt-4o")
    
    def get_available_models(self) -> List[Dict[str, str]]:
        """Get list of available models based on provider"""
        if self.provider == "lmstudio":
            return self._get_lmstudio_models()
        elif self.provider == "ollama":
            return self._get_ollama_models()
        elif self.provider == "openai":
            return self._get_openai_models()
        else:
            return []
    
    def _get_lmstudio_models(self) -> List[Dict[str, str]]:
        """Fetch available models from LM Studio"""
        try:
            response = requests.get(f"{self.base_url}/models", timeout=5)
            response.raise_for_status()
            models_data = response.json()
            
            models = []
            for model in models_data.get("data", []):
                models.append({
                    "id": model.get("id", ""),
                    "name": model.get("id", ""),
                    "provider": "lmstudio"
                })
            
            return models
        except Exception as e:
            st.warning(f"Could not fetch LM Studio models: {e}")
            return []
    
    def _get_ollama_models(self) -> List[Dict[str, str]]:
        """Fetch available models from Ollama"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            models_data = response.json()
            
            models = []
            for model in models_data.get("models", []):
                models.append({
                    "id": model.get("name", ""),
                    "name": model.get("name", ""),
                    "provider": "ollama"
                })
            
            return models
        except Exception as e:
            st.warning(f"Could not fetch Ollama models: {e}")
            return []
    
    def _get_openai_models(self) -> List[Dict[str, str]]:
        """Return common OpenAI models"""
        return [
            {"id": "gpt-4o", "name": "GPT-4o", "provider": "openai"},
            {"id": "gpt-4o-mini", "name": "GPT-4o Mini", "provider": "openai"},
            {"id": "gpt-4-turbo", "name": "GPT-4 Turbo", "provider": "openai"},
            {"id": "gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "provider": "openai"}
        ]
    
    def set_model_for_type(self, model_type: str, model_id: str):
        """Set the model for a specific type and save to config"""
        if "llm_models" not in self.config:
            self.config["llm_models"] = {"chat": None, "lesson": None, "available": []}
        
        self.config["llm_models"][model_type] = model_id
        save_config(self.config)
        
        # Update current model if it matches the type
        if self.model_type == model_type:
            self.model = model_id
    
    def refresh_available_models(self):
        """Refresh and cache available models"""
        available_models = self.get_available_models()
        if "llm_models" not in self.config:
            self.config["llm_models"] = {"chat": None, "lesson": None, "available": []}
        
        self.config["llm_models"]["available"] = available_models
        save_config(self.config)
        return available_models
    
    def chat_completion(self, messages, temperature=None, max_tokens=None, model=None):
        """Generate chat completion using the configured provider"""
        
        # Use instance defaults if not specified
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens
        model_name = model if model is not None else self.model
        
        try:
            if self.provider == "ollama":
                return self._ollama_completion(messages, temp, tokens, model_name)
            else:
                # Both OpenAI and LM Studio use the same API format
                response = self.client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=temp,
                    max_tokens=tokens
                )
                return response.choices[0].message.content
                
        except Exception as e:
            error_msg = f"Error with {self.provider}: {str(e)}"
            st.error(error_msg)
            raise Exception(error_msg)
    
    def _ollama_completion(self, messages, temperature, max_tokens, model):
        """Handle Ollama API calls"""
        
        # Convert messages to Ollama format
        prompt = self._convert_messages_to_prompt(messages)
        
        url = f"{self.base_url}/api/generate"
        data = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "")
    
    def _convert_messages_to_prompt(self, messages):
        """Convert OpenAI message format to simple prompt for Ollama"""
        prompt_parts = []
        
        for message in messages:
            role = message.get("role", "")
            content = message.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"Human: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        # Add final prompt for assistant response
        prompt_parts.append("Assistant:")
        
        return "\n\n".join(prompt_parts)
    
    def get_provider_info(self):
        """Return information about current provider configuration"""
        return {
            "provider": self.provider,
            "model": self.model,
            "model_type": self.model_type,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "base_url": getattr(self, "base_url", None)
        }

# Global instances
_llm_clients = {}

def get_llm_client(model_type: str = "chat"):
    """Get or create LLM client instance for specific model type"""
    global _llm_clients
    if model_type not in _llm_clients:
        _llm_clients[model_type] = LLMClient(model_type)
    return _llm_clients[model_type]

def chat_completion(messages, temperature=None, max_tokens=None, model=None, model_type="chat"):
    """Convenience function for chat completion"""
    client = get_llm_client(model_type)
    return client.chat_completion(messages, temperature, max_tokens, model)

def get_available_models():
    """Get available models for the current provider"""
    client = get_llm_client()
    return client.get_available_models()

def set_model_for_type(model_type: str, model_id: str):
    """Set model for a specific type"""
    # Clear existing client for this type to force recreation
    global _llm_clients
    if model_type in _llm_clients:
        del _llm_clients[model_type]
    
    # Create new client and set the model
    client = get_llm_client(model_type)
    client.set_model_for_type(model_type, model_id)

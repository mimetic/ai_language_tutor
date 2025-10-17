# AI Language Tutor

## 📌 Project Overview
AI Language Tutor is a personal AI-powered language learning assistant built using **Streamlit** and **OpenAI's GPT models**. The app provides structured language learning with lesson plans, vocabulary tracking, quizzes, and AI-driven conversational practice.

Check out full story in my [Medium article](https://medium.com/@kate.ruksha/building-an-ai-powered-personal-language-tutor-with-chatgpt-59d2e4cd7f56).

## 🚀 Features
- **AI Chatbot Tutor** – Engage in real-time AI-powered conversations.
- **Lesson Plans** – Auto-generated structured learning plans.
- **Vocabulary Management** – Store, review, and practice new words.
- **Quizzes** – AI-generated quizzes based on stored vocabulary.
- **Lesson History** – Review past conversations and learning progress.
- **Multi-Model Support** – Choose different LLM models for chat and lesson planning.
- **Model Discovery** – Automatically discover available models from LM Studio.
- **Centralized Settings** – Configure models, language, and view system info in dedicated Settings page.

## 🏗️ Tech Stack
- **Frontend:** Streamlit (Fast UI prototyping)
- **Backend:** Multi-LLM support (OpenAI API, LM Studio, Ollama)
- **Data Storage:** Local JSON files (User history, vocabulary, lesson plans, model configurations)
- **Customization:** CSS/HTML for UI enhancements

## 📂 Folder Structure
```plaintext
AI_LANGUAGE_TUTOR/
│── assets/                # Stores user data
│   │── chat_history.json      # Stores conversation history
│   │── lesson_plan_inputs.json  # Inputs for lesson planning
│   │── lesson_plan.json        # Saved lesson plans
│   │── user_vocabulary.json    # User's vocabulary list
│
│── pages/                # Streamlit UI pages
│   │── chatbot.py         # AI chatbot interface
│   │── history.py         # Lesson history page
│   │── lesson_plan.py     # Lesson plan page
│   │── settings.py        # Settings and configuration page
│   │── vocab.py           # Vocabulary management page
│
│── components/            # Reusable UI components
│   │── model_selector.py  # Model selection interface
│
│── utils/                 # Utility functions and configurations
│   │── config.json        # Stores configuration settings (language, models)
│   │── llm_client.py      # Multi-provider LLM client
│   │── storage.py         # Handles saving/loading data
│
│── .gitignore             # Ignore unnecessary files
│── app.py                 # Main Streamlit entry point
│── sidebar.py             # Sidebar navigation
│── README.md              # Project documentation
```

## 🛠️ Setup & Installation
### **Configuring the AI Model & Learning Language**

#### **Model Selection**
The app supports multiple LLM providers:
- **OpenAI**: GPT-4o, GPT-4o Mini, GPT-4 Turbo, GPT-3.5 Turbo
- **LM Studio**: Auto-discovery of local models
- **Ollama**: Auto-discovery of local models

#### **Configuration Options**
1. **Environment Variables** (`.env` file):
   ```bash
   # Provider selection
   LLM_PROVIDER=lmstudio  # or openai, ollama
   
   # Separate models for different functions
   LLM_MODEL_CHAT=qwen2.5-7b-instruct
   LLM_MODEL_LESSON=qwen2.5-7b-instruct
   
   # LM Studio/Ollama configuration
   LMSTUDIO_BASE_URL=http://localhost:1234/v1
   OLLAMA_BASE_URL=http://localhost:11434
   
   # OpenAI configuration
   OPENAI_API_KEY=your-api-key-here
   ```

2. **Settings Page**: Access the Settings page (⚙️ icon) to:
   - Choose different models for chat vs lesson planning
   - Auto-discover available models from LM Studio
   - Switch models without restarting the app
   - Change learning language
   - View prompt configurations

3. **Language Configuration**: Set in `utils/config.json`:
   ```json
   {
     "language": "German",
     "llm_models": {
       "chat": "model-name",
       "lesson": "model-name"
     }
   }
   ```


### **Prerequisites**
Ensure you have **Python 3.8+** installed.

### **Installation Steps**
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/your-repo/AI-Language-Tutor.git
   cd AI-Language-Tutor
   ```
2. **Create a Virtual Environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```
3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Setup Environment:**
   ```sh
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env with your configuration
   # Set your API keys and preferred models
   ```
5. **Run the App:**
   ```sh
   streamlit run app.py
   ```

## 📖 Usage Guide
1. **Start the app** and select an activity from the main page.
2. **Configure settings** using the Settings page (⚙️ icon):
   - Choose different models for chat and lesson planning
   - Change learning language
   - View prompt configurations and system info
   - Refresh to discover new models from LM Studio
3. **Use the AI Chat** for practice and receive instant corrections.
4. **Generate lesson plans** tailored to your language goals.
5. **Add new words** to your vocabulary list for later review.
6. **Take quizzes** to reinforce learning.
7. **Review past conversations** in the history tab.

## 🎯 Future Improvements
- ✅ Text-to-speech integration for listening practice.
- ✅ Speech-to-text integration for pronunciation practice.
- ✅ Explore improvements with Agentic AI.

## 👨‍💻 Author
**Katsiaryna Ruksha**  
Feel free to connect on [LinkedIn](https://www.linkedin.com/in/katsiaryna-ruksha-81b9837b/) or contribute to the project!

---
🔹 *AI Language Tutor - Making Language Learning Smarter!*


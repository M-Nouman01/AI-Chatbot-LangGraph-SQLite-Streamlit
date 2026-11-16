# 🤖 AI Assistant ChatBot with LangGraph, Gemini & SQLite

A full-stack, persistent conversational AI web application built using **LangGraph**, **Google Gemini**, **SQLite** for state persistence, and **Streamlit** for the interactive user interface.

## ✨ Key Features

1. **Persistent Chat History (SQLite Integration):** 
   - Replaced in-memory storage with `SqliteSaver` so your chat threads, messages, and state are safely saved across restarts.
2. **Resume & Manage Multiple Chats:** 
   - View past conversation threads in a sidebar, switch between them instantly, and seamlessly resume previous chats.
3. **Real-time Response Streaming:** 
   - Uses LangGraph's streaming capabilities combined with Streamlit's `st.write_stream` to render Gemini's token chunks dynamically.
4. **Google Gemini Integration:** 
   - Powered by Google's latest generative AI models with robust handling for multimodal message blocks and plain-text conversion.

## 🛠️ Tech Stack
- **Orchestration:** LangGraph (`StateGraph`, `SqliteSaver`, `add_messages`)
- **LLM:** Google Generative AI (`ChatGoogleGenerativeAI` / Gemini)
- **Frontend & UI:** Streamlit
- **Database:** SQLite (`chatbot.db`)

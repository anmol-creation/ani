# .ac Personal AI Assistant (Local Ecosystem Brain)

Welcome to the **.ac Ecosystem**, a completely free, 100% local, and API-less personalized AI assistant designed specifically to act as the central brain for all your projects.

This project is built to run entirely on a **Samsung Galaxy S23 using Samsung DeX**, ensuring full privacy and a mobile-first AI development environment. It understands both **Hindi and English**, making it a truly localized and personal assistant.

## 🧠 Core Concept

The goal is to create a "Second Brain" that connects to all your different repositories and projects. By maintaining a deep context of your entire codebase, this AI will help you:
- Discuss ideas privately.
- Keep track of project structures and data.
- Deeply understand your coding style and architecture.
- Seamlessly sync and integrate multiple projects together.

## 🏗 Architecture Blueprint

The system is built on a **Local RAG (Retrieval-Augmented Generation) + Agentic System** architecture.

### 1. Local AI Engine (The Brain)
- **Engine:** `Ollama` or `Llama.cpp` compiled within Termux (Android).
- **Models (SLMs):** Lightweight yet capable models like **Qwen 2.5 (1.5B/3B)**, **Llama 3.2 (1B/3B)**, or **Gemma 2 (2B)** in quantized (GGUF) formats to run efficiently on mobile hardware (ARM architecture).

### 2. Memory & Context (The Knowledge Base)
- **Vector Database:** A lightweight, local vector DB like **ChromaDB** or **FAISS** running locally via Python.
- **Data Ingestion:** Scripts to scan your `.ac` ecosystem and other local repositories (Markdown, JS, Python files), chunk the text, and generate embeddings using local models (e.g., `all-MiniLM-L6-v2`).
- **Retrieval System:** When queried, the system searches the Vector DB to provide context to the LLM before generating a response.

### 3. Agentic Capabilities
- The AI will have access to "Tools" to interact with the local file system:
  - Read specific files.
  - Scan directories and Git histories.
  - Cross-reference code between different repositories.

### 4. Development Environment (Mobile/DeX)
- **Environment:** Termux (Linux environment on Android).
- **Logic & RAG Pipeline:** Python (using LangChain or LlamaIndex).
- **Interface:** A local web server (FastAPI/Flask) served to the browser on localhost, acting as the chat interface.
- **Editor:** Acode or Termux-Neovim for coding within Samsung DeX.

## 🚀 Setup Flow (Work In Progress)

1. **Environment Setup:** Configure Termux, Python, and necessary dependencies on the device.
2. **LLM Engine Installation:** Setup Ollama/Llama.cpp to run quantized models locally.
3. **Database Initialization:** Set up the local Vector Database.
4. **Data Ingestion Pipeline:** Create scripts to feed local project files into the DB.
5. **RAG Integration:** Connect the LLM with the Vector DB using an orchestration framework (LangChain/LlamaIndex).
6. **UI/Interface Creation:** The project now includes a built-in Dark Mode Chat UI designed for Samsung DeX.

## 💻 Web App Interface

The FastAPI server now directly serves the frontend web application. Once the server is running, simply open your browser and navigate to:
**[http://localhost:8000](http://localhost:8000)**

This will load the `.ac` Personal AI chat interface.

---
*Note: This project is under active development and relies entirely on open-source, on-device tools to guarantee absolute privacy and zero recurring costs.*

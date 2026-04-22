# 🤖 Nexa AI Chatbot

An advanced **AI-powered chatbot** built with **Streamlit, LangChain, and Groq (LLaMA 3.1)** that can:

* 📄 Understand documents (PDFs & images)
* 🌐 Answer general questions (like ChatGPT)

---

## 🚀 Live Demo

👉 (https://ai-chatbot-app-vkei.onrender.com)

---

## 📌 Project Overview

Nexa AI Chatbot is a smart assistant that supports **dual-mode interaction**:

### 📄 Document-Based Q&A

* Upload PDFs or images
* Extract text using OCR
* Ask questions based on document content

### 🌐 General AI Chat

* Ask any question without uploading a document
* Get answers using general knowledge

The chatbot automatically detects the query type and switches between:

* **RAG (for documents)**
* **LLM general reasoning (for normal queries)**

---

## ✨ Key Features

### 📄 Document Understanding

* Supports **PDF files**
* Supports **image-based documents**
* Extracts text using OCR API

### 🧠 Context-Aware AI (RAG)

* Custom chunk-based retrieval system
* Matches query keywords with document content
* Returns only relevant context to the LLM

### 🌐 General AI Chat Mode

* Answers general questions without documents
* Works like a normal AI assistant
* No dependency on uploaded files

### 💬 Smart Chat System

* Interactive chat interface
* Maintains conversation history
* Supports follow-up questions

### ⚡ High-Speed AI Responses

* Powered by **Groq LLaMA 3.1 (8B Instant)**

### 📥 Export Feature

* Download full chat history as PDF

---

## ⚙️ How It Works

### 📄 Document Mode (RAG)

1. Upload document
2. Extract text (PDF/OCR)
3. Split into chunks
4. Retrieve relevant chunks
5. Pass context to LLM
6. Generate answer

### 🌐 General Mode

1. Ask any question
2. LLM processes query
3. Returns answer

---

## 🧪 Example Questions

### 📄 Document-Based

* "Summarize this document"
* "Explain this in short"
* "What are key points?"

### 🌐 General Questions

* "Who is Virat Kohli?"
* "Explain AI"
* "What is Python?"

---

## 🛠️ Tech Stack

* Streamlit
* Python
* LangChain
* Groq (LLaMA)
* OCR.space API
* PyPDF
* ReportLab

---

## ▶️ Run Locally

```bash
git clone https://github.com/your-username/nexa-ai-chatbot.git
cd nexa-ai-chatbot
pip install -r requirements.txt
streamlit run app.py
```

---

## 👨‍💻 Author

**Yashodip Salunkhe**

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!

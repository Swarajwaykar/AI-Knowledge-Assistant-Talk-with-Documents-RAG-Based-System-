# 🧠 AI Knowledge Assistant- Talk with Documents (RAG-Based System)

An end-to-end Retrieval-Augmented Generation (RAG) system for intelligent document-based question answering.

---

## 🚀 Features

* 📄 Multi-format document ingestion (PDF, TXT, CSV, JSON)
* 🔍 Semantic search using FAISS
* 🧠 Embedding-based retrieval with Sentence Transformers
* 🤖 LLM-powered response generation (Groq / LLaMA 3.1)
* ⚡ Fast and scalable pipeline
* 🎯 Reduced hallucination via context grounding

---

## 🏗️ Architecture

1. Load documents
2. Split into chunks
3. Generate embeddings
4. Store in FAISS
5. Retrieve top-k results
6. Generate answer using LLM

---

## 🛠️ Tech Stack

* Python
* LangChain
* FAISS
* Sentence Transformers
* Groq API (LLM)
* FastAPI / Streamlit (optional UI)

---

## ▶️ Run Locally

```bash
git clone https://github.com/your-username/rag-project.git
cd rag-project

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
python app.py
```

---

## 📌 Example Query

> "What is Emotion Detection?"

---

## 📈 Future Improvements

* Add chat memory
* UI with Streamlit
* API deployment
* Source citations

---

## 👨‍💻 Author

Swaraj Waykar

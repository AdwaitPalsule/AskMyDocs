# 📚 AskMyDocs – Multi-Document Q&A Chatbot (Ollama + HuggingFace )

AskMyDocs is a **multi-document question answering** chatbot that:
- Lets you **upload multiple documents** (`PDF`, `TXT`, `DOCX`).
- Uses **HuggingFace embeddings** to create a searchable vector database.
- Uses **LLaMA 3.2** from **Ollama** for answer generation.
- Stores **chat history** in a **SQLite database** so you can keep conversations.

---

## 🚀 Features
- **Document Upload**: Upload PDFs, TXT, or DOCX files.
- **Automatic Document Processing**: Extracts text and creates embeddings.
- **RAG (Retrieval-Augmented Generation)**: Retrieves relevant chunks before answering.
- **Local LLM**: Uses Ollama’s LLaMA 3.2 model.
- **Persistent Chat History**: Saved per session using SQLite.

---

## 📂 Folder Structure
```
AskMyDocs/
│── app.py               # Main Streamlit app
│── requirements.txt     # Python dependencies
│── README.md            # Project documentation
│── uploaded_docs/       # Uploaded user documents
│
├── src/
│   ├── qa_chain.py      # Loads embeddings, processes docs, runs RAG
│   ├── db.py            # SQLite chat history functions
│   ├── __init__.py
│
└── .gitignore           # Files to ignore in Git
```

---

## 🛠 Installation & Setup

### 1️⃣ Clone the repository
```
git clone https://github.com/yourusername/AskMyDocs.git
cd AskMyDocs
```

### 2️⃣ Create a virtual environment
```
python -m venv venv
source venv/bin/activate    # On Linux/Mac
venv\Scripts\activate       # On Windows
```

### 3️⃣ Install dependencies
```
pip install -r requirements.txt
```

### 4️⃣ Install & run Ollama
- Download Ollama: [https://ollama.ai/download](https://ollama.ai/download)
- Pull the LLaMA 3.2 model:
```
ollama pull llama3.2
```

---

## ▶ Running the App
```
streamlit run app.py
```

---



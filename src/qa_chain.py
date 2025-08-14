import requests
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
import os


def load_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def process_documents(doc_paths, embeddings):
    all_docs = []
    for path in doc_paths:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(path)
        elif ext == ".txt":
            loader = TextLoader(path)
        elif ext in [".docx", ".doc"]:
            loader = Docx2txtLoader(path)
        else:
            continue
        all_docs.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    split_docs = text_splitter.split_documents(all_docs)

    vectorstore = FAISS.from_documents(split_docs, embeddings)
    return vectorstore


def retrieve_relevant_docs(vectorstore, query, k=3):
    return vectorstore.similarity_search(query, k=k)


def load_llama():
    """
    Just return model name since we're using Ollama locally.
    """
    return "llama3.2"


# Ask Ollama

def answer_question_ollama(model_name, context, question):
    prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model_name, "prompt": prompt, "stream": False}
    )
    try:
        data = response.json()
        return data.get("response", "").strip()
    except Exception:
        return "Error: Could not get a valid response from Ollama."

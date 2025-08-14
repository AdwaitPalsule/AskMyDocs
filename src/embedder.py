from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from config import EMBEDDING_MODEL

def embed_documents(splitted_docs):
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(splitted_docs, embeddings)
    return vectorstore

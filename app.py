import streamlit as st
import os
import uuid
from src.db import init_db, save_message, get_chat_history, get_all_sessions
from src.qa_chain import (
    load_embeddings,
    process_documents,
    retrieve_relevant_docs,
    load_llama,
    answer_question_ollama
)

st.set_page_config(page_title="Multi-Document Q&A", layout="wide")
st.title("📚 Multi-Document Q&A Chatbot ")


init_db()


if "user_id" not in st.session_state:
    st.session_state.user_id = "user_123"  

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "embeddings" not in st.session_state:
    st.session_state.embeddings = load_embeddings()

if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "llm" not in st.session_state:
    st.session_state.llm = load_llama()


with st.sidebar:
    st.header(f"💬 Conversations for {st.session_state.user_id}")
    sessions = get_all_sessions(st.session_state.user_id)
    selected_session = st.selectbox(
        "Select a conversation:",
        options=sessions,
        index=0 if sessions else None
    )

    if st.button("➕ New Conversation"):
        st.session_state.session_id = str(uuid.uuid4())

    if selected_session:
        st.session_state.session_id = selected_session


uploaded_files = st.file_uploader(
    "Upload documents (PDF, TXT, DOCX)",
    type=["pdf", "txt", "docx"],
    accept_multiple_files=True
)

if uploaded_files:
    doc_paths = []
    os.makedirs("uploaded_docs", exist_ok=True)
    for file in uploaded_files:
        file_path = os.path.join("uploaded_docs", file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())
        doc_paths.append(file_path)

    with st.spinner("Processing documents..."):
        st.session_state.vectorstore = process_documents(
            doc_paths,
            st.session_state.embeddings
        )

    st.success("✅ Documents processed and ready!")


history = get_chat_history(st.session_state.user_id, st.session_state.session_id)
if history:
    for msg in history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

query = st.chat_input("Ask a question about your documents:")

if query and st.session_state.vectorstore is not None:
    with st.chat_message("user"):
        st.markdown(query)

    save_message(st.session_state.user_id, st.session_state.session_id, "user", query)

    with st.spinner("Searching and generating answer..."):
        retrieved_docs = retrieve_relevant_docs(st.session_state.vectorstore, query)
        context = "\n\n".join([doc.page_content for doc in retrieved_docs])
        answer = answer_question_ollama(st.session_state.llm, context, query)

    with st.chat_message("assistant"):
        st.markdown(answer)

    save_message(st.session_state.user_id, st.session_state.session_id, "assistant", answer)

    with st.expander("📄 Retrieved Document Chunks"):
        for i, doc in enumerate(retrieved_docs, 1):
            st.markdown(f"**Chunk {i}:** {doc.page_content}")

elif query and st.session_state.vectorstore is None:
    st.warning("⚠️ Please upload and process documents first.")

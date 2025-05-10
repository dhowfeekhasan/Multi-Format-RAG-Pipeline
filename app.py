import streamlit as st

# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Document QA", layout="wide")

import os
import shutil
from file_processor import process_file
from rag_processor import RAGProcessor
from main import generate_answer  # Reuse your backend logic

# Define folder paths
EXTRACTED_FOLDER = "extracted_data"
UPLOADS_FOLDER = "uploads"

# Function to clear all files in a folder
def clear_folder(folder_path):
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)

# Initialize RAG Processor
rag_processor = RAGProcessor()
indexed = False

st.title("📄 RAG System")

# Upload Section
st.header("1. Upload a Document")
uploaded_file = st.file_uploader("Upload a new document", type=["pdf", "docx", "pptx", "png", "jpg", "jpeg"])

if uploaded_file:
    with st.spinner("🔄 Clearing previous uploads and data..."):
        clear_folder(EXTRACTED_FOLDER)
        clear_folder(UPLOADS_FOLDER)

    file_path = os.path.join(UPLOADS_FOLDER, uploaded_file.name)
    os.makedirs(UPLOADS_FOLDER, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with st.spinner(" Processing and indexing file..."):
        txt_file_path, _ = process_file(file_path, document_type=None)  # document_type removed
        if txt_file_path:
            indexed = rag_processor.index_documents()
            if indexed:
                st.success("File processed and indexed successfully!")
            else:
                st.error(" Failed to index the document.")
        else:
            st.error("File processing failed.")

# Query Section
st.header("2. Ask a Question")
query = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if not indexed:
        st.warning(" Please upload and process a document first.")
    else:
        with st.spinner("🔍 Retrieving relevant information..."):
            results = rag_processor.retrieve(query)

            if results:
                st.subheader("processing...")
                context = "\n".join([doc.get("text_data", "") for doc in results])
                answer = generate_answer(query, context)

                st.subheader("💬 Answer")
                st.markdown(f"**{answer.strip()}**")
            else:
                st.error("❌ No relevant information found.")

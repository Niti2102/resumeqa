import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_documents(file_path):
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()
    return documents

def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    return chunks

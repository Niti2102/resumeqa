import os
from langchain_core.documents import Document

def load_documents(file_path="personal_info.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return [Document(page_content=text)]

def split_documents(documents):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    # Use a large chunk size since the file is small
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=0)
    return text_splitter.split_documents(documents)

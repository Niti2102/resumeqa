import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from utils import load_documents, split_documents
from config import vector_store_path

# Load and split the personal info text file
file_path = "personal_info.txt"
documents = load_documents(file_path)
chunks = split_documents(documents)

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create FAISS vector store
db = FAISS.from_documents(chunks, embedding_model)

# Save vector store
db.save_local(vector_store_path)
print("✅ Personal info embedded and FAISS vector store saved!")

import os
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from utils import load_documents, split_documents
from config import vector_store_path

# Path to your resume PDF file
resume_path = os.path.join(os.path.dirname(__file__), "resume.pdf")

# Load and split the documents
documents = load_documents(resume_path)
chunks = split_documents(documents)

# Initialize embedding model
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create FAISS vector store
db = FAISS.from_documents(chunks, embedding_model)

# Save vector store
db.save_local(vector_store_path)

print("✅ Resume embedded and FAISS vector store saved!")

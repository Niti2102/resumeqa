from flask import Flask, request, jsonify
from utils import load_documents, split_documents
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os

app = Flask(__name__)

# Load and split personal info
file_path = os.path.join(os.path.dirname(__file__), '../personal_info.txt')
documents = load_documents(file_path)
chunks = split_documents(documents)
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.from_documents(chunks, embedding_model)
retriever = db.as_retriever(search_kwargs={"k": 5})

@app.route("/api", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    docs = retriever.get_relevant_documents(question)
    context = "\n".join([doc.page_content for doc in docs])
    # You can add LLM completion here if you want
    return jsonify({"answer": context})

# For Vercel
app = app 
import os
from flask import Flask, render_template, request, jsonify
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
from langchain.chains import ConversationalRetrievalChain
from config import vector_store_path

app = Flask(__name__)

# Load the vector store with smaller model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-MiniLM-L3-v2")
db = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)

# Set up the conversational retrieval chain
chat = ChatGroq(temperature=0, model_name="llama3-8b-8192")
retriever = db.as_retriever(search_kwargs={"k": 2})

# Define the prompt template
prompt_template = """
Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=prompt_template)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=chat,
    retriever=retriever,
    combine_docs_chain_kwargs={'prompt': QA_CHAIN_PROMPT},
    return_source_documents=True
)

chat_history = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    query = request.json["query"]
    result = qa_chain({"question": query, "chat_history": chat_history})
    chat_history.append((query, result["answer"]))
    return jsonify({"response": result["answer"]})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
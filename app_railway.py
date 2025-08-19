from flask import Flask, render_template, request, jsonify
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from config import vector_store_path
import os

app = Flask(__name__)

# Global variables for lazy loading
embeddings = None
db = None
qa_chain = None
chat_history = []

def load_models():
    """Lazy load models only when needed"""
    global embeddings, db, qa_chain
    
    if embeddings is None:
        # Use a lighter embedding model
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    
    if db is None:
        try:
            # Use ChromaDB instead of FAISS for better compatibility
            db = Chroma(persist_directory=vector_store_path, embedding_function=embeddings)
            print("Loaded ChromaDB vector store")
        except Exception as e:
            print(f"ChromaDB loading failed: {e}")
            # Create a simple in-memory fallback
            from langchain_community.vectorstores import InMemoryVectorStore
            db = InMemoryVectorStore(embedding=embeddings)
            print("Using in-memory vector store")
    
    if qa_chain is None:
        # Set up the conversational retrieval chain
        chat = ChatGroq(temperature=0, model_name="llama3-8b-8192")
        retriever = db.as_retriever(search_kwargs={"k": 2})

        # Define the prompt template
        prompt_template = """
        Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    # Load models on first request
    load_models()
    
    query = request.json["query"]
    result = qa_chain({"question": query, "chat_history": chat_history})
    chat_history.append((query, result["answer"]))
    return jsonify({"response": result["answer"]})

if __name__ == "__main__":
    app.run(debug=True)

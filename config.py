import os

# Get the absolute path of the directory where the current file is located
current_directory = os.path.dirname(os.path.abspath(__file__))

# Set the GROQ_API_KEY environment variable
os.environ["GROQ_API_KEY"] = "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"

# Define the path for the vector store
vector_store_path = os.path.join(current_directory, "faiss_index") 
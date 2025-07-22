import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the absolute path of the directory where the current file is located
current_directory = os.path.dirname(os.path.abspath(__file__))

# Fetch the GROQ_API_KEY from environment
groq_api_key = os.getenv("GROQ_API_KEY")

# Optional: raise an error if the key is missing
if not groq_api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

# Define the path for the vector store
vector_store_path = os.path.join(current_directory, "faiss_index")

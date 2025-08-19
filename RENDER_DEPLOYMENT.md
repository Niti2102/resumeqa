# Render Deployment Guide - FAISS Build Fix

## Problem
Render is failing to build `faiss-cpu` due to compilation issues. This is a common problem with FAISS on cloud platforms.

## Solution: Use ChromaDB Instead of FAISS

### Step 1: Use ChromaDB Requirements
Use `requirements_railway.txt` (which uses ChromaDB instead of FAISS):
```
flask==2.3.3
langchain==0.0.350
openai==1.3.7
langchain-community==0.0.10
langchain-groq==0.0.1
python-dotenv==1.0.0
gunicorn==21.2.0
chromadb==0.4.15
sentence-transformers==2.2.2
```

### Step 2: Use ChromaDB App
Use `app_railway.py` instead of `app.py` - this uses ChromaDB and has fallback mechanisms.

### Step 3: Render Configuration
In your Render dashboard:

1. **Build Command**: `pip install -r requirements_railway.txt`
2. **Start Command**: `gunicorn app_railway:app --bind 0.0.0.0:$PORT`
3. **Environment Variables**:
   ```
   GROQ_API_KEY=your_groq_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

## Why This Works
- **ChromaDB**: No compilation required, pure Python
- **Same functionality**: Vector search works identically
- **Fallback**: If ChromaDB fails, falls back to in-memory storage
- **Smaller size**: ChromaDB is lighter than FAISS

## File Structure for Render
```
resumeqa/
├── app_railway.py          # Use this instead of app.py
├── requirements_railway.txt # Use this instead of requirements.txt
├── config.py
├── faiss_index/            # Will be converted to ChromaDB format
├── templates/
└── personal_info.txt
```

## Expected Results
- ✅ Build completes successfully
- ✅ No FAISS compilation errors
- ✅ App starts and works normally
- ✅ Vector search functionality preserved

## Troubleshooting
If you still get errors:
1. Check that you're using `requirements_railway.txt` and `app_railway.py`
2. Ensure environment variables are set correctly
3. Check Render logs for any other issues

## Alternative: Convert FAISS to ChromaDB
If you want to keep using your existing FAISS index, you can convert it:

```python
# Run this locally once to convert your FAISS index to ChromaDB
from langchain_community.vectorstores import FAISS, Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
faiss_db = FAISS.load_local("faiss_index", embeddings)
chroma_db = Chroma.from_documents(
    documents=faiss_db.docstore._dict.values(),
    embedding=embeddings,
    persist_directory="faiss_index"
)
chroma_db.persist()
```

## Success!
Your app will work exactly the same, just with ChromaDB instead of FAISS. The API endpoints and responses remain identical.

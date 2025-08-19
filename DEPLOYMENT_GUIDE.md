# Deployment Guide - Size Optimization

## Problem
Your Flask app is hitting size constraints on deployment platforms like Render due to large dependencies, especially the sentence-transformers library and embedding models.

## Solutions Implemented

### 1. Optimized Requirements
- **Original**: Unversioned packages that could pull latest (larger) versions
- **Fixed**: Pinned specific versions to control size
- **Added**: `gunicorn` for production deployment

### 2. Lazy Loading
- **Problem**: Models loaded at startup, increasing memory usage
- **Solution**: Models now load only when first request is made
- **Benefit**: Faster startup, lower initial memory usage

### 3. Lightweight Alternative
- **File**: `requirements_lightweight.txt`
- **Replaces**: `sentence-transformers` with `scikit-learn`
- **Size reduction**: ~200-300MB smaller

### 4. Docker Optimization
- **Added**: `.dockerignore` to exclude unnecessary files
- **Excludes**: Cache files, virtual environments, IDE files, etc.

## Deployment Options

### Option 1: Render (Recommended)
1. Use `requirements.txt` (optimized version)
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `gunicorn app:app --bind 0.0.0.0:$PORT`

### Option 2: Render with Lightweight Dependencies
1. Use `requirements_lightweight.txt`
2. Modify `app.py` to use scikit-learn embeddings
3. Set build command: `pip install -r requirements_lightweight.txt`

### Option 3: Railway
1. Similar to Render setup
2. Better for larger applications
3. More generous size limits

### Option 4: Heroku
1. Use `requirements.txt`
2. Add `Procfile` with: `web: gunicorn app:app`
3. Note: Heroku has been discontinued for free tier

## Environment Variables
Make sure to set these in your deployment platform:
```
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Additional Optimizations

### 1. Use Smaller Embedding Model
If still hitting limits, consider:
```python
# In app.py, replace the embedding model with:
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-MiniLM-L3-v2",  # Even smaller
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)
```

### 2. Pre-download Models
For faster deployment, pre-download models locally and include them in your repo:
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### 3. Use External Vector Database
Consider using Pinecone or Weaviate instead of local FAISS:
- Reduces deployment size
- Better scalability
- Pay-per-use pricing

## Troubleshooting

### Build Fails Due to Size
1. Try `requirements_lightweight.txt`
2. Check if you can upgrade to a paid plan
3. Consider splitting into microservices

### Memory Issues
1. Ensure lazy loading is working
2. Monitor memory usage in deployment logs
3. Consider reducing `k` value in retriever

### Model Download Issues
1. Check internet connectivity during build
2. Consider pre-downloading models
3. Use smaller models

## File Structure for Deployment
```
your-app/
├── app.py
├── config.py
├── requirements.txt (or requirements_lightweight.txt)
├── .dockerignore
├── faiss_index/
│   ├── index.faiss
│   └── index.pkl
├── templates/
│   └── index.html
└── personal_info.txt
```

## Success Metrics
- Build time: < 10 minutes
- Deployment size: < 500MB
- Startup time: < 30 seconds
- Memory usage: < 512MB

# Railway Deployment Guide - FAISS Build Fix

## Problem
Railway is failing to build `faiss-cpu` due to compilation issues in the Docker environment.

## Solutions (Try in Order)

### Solution 1: Use faiss-cpu-noavx2 (Recommended)
1. Use the updated `requirements.txt` with `faiss-cpu-noavx2==1.7.4`
2. This version is more compatible with Railway's build environment

### Solution 2: Use ChromaDB Alternative
1. Use `requirements_railway.txt` instead of `requirements.txt`
2. Use `app_railway.py` instead of `app.py`
3. This completely avoids FAISS and uses ChromaDB

### Solution 3: Railway Configuration
In your Railway project settings:
1. **Build Command**: `pip install -r requirements_railway.txt`
2. **Start Command**: `gunicorn app_railway:app --bind 0.0.0.0:$PORT`
3. **Environment Variables**: Set your API keys

## Step-by-Step Railway Deployment

### Option A: With FAISS (if Solution 1 works)
1. Use `requirements.txt` (updated with faiss-cpu-noavx2)
2. Use `app.py` (original)
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

### Option B: With ChromaDB (if FAISS fails)
1. Use `requirements_railway.txt`
2. Use `app_railway.py`
3. Build Command: `pip install -r requirements_railway.txt`
4. Start Command: `gunicorn app_railway:app --bind 0.0.0.0:$PORT`

## Environment Variables
Set these in Railway:
```
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
```

## Troubleshooting

### If Build Still Fails:
1. **Check Railway logs** for specific error messages
2. **Try Solution 2** (ChromaDB) if FAISS continues to fail
3. **Consider Render** as an alternative (often more forgiving with builds)

### If App Starts But Vector Search Fails:
1. The `app_railway.py` has fallback mechanisms
2. It will try FAISS → ChromaDB → In-Memory
3. Check logs to see which vector store is being used

## File Structure for Railway
```
resumeqa/
├── app_railway.py          # Railway-compatible app
├── app.py                  # Original app
├── requirements_railway.txt # Railway requirements
├── requirements.txt        # Original requirements
├── config.py
├── faiss_index/
├── templates/
└── personal_info.txt
```

## Success Indicators
- ✅ Build completes without FAISS errors
- ✅ App starts successfully
- ✅ Vector search works (check logs for which store is used)
- ✅ API responds to requests

## Alternative Platforms
If Railway continues to have issues:
1. **Render**: Often more forgiving with builds
2. **Heroku**: Good for smaller apps
3. **DigitalOcean App Platform**: Good for larger apps

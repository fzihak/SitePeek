# 🚀 How to Deploy SitePeek to Vercel - Quick Guide

## Overview

SitePeek has:
- **Frontend** (HTML/CSS/JS) → Deploy to **Vercel** ✅
- **Backend** (Python/FastAPI) → Deploy to **Railway** or **Render** ✅

---

## 📝 Simple 3-Step Process

### Step 1️⃣: Push to GitHub

```powershell
# Run this in PowerShell
cd "D:\Self Project\SitePeek"

# Run the setup script
.\setup-git.ps1

# Then create GitHub repo and push (follow instructions from script)
```

---

### Step 2️⃣: Deploy Backend (Choose One)

#### Option A: Railway (Recommended - Easy)

1. Go to https://railway.app/
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `SitePeek` repository
5. Settings:
   - **Root Directory**: `backend`
   - Click Deploy
6. **Copy your Railway URL** (e.g., `https://sitepeek-production.up.railway.app`)

#### Option B: Render (Free Tier)

1. Go to https://render.com/
2. New → Web Service
3. Connect your GitHub `SitePeek` repo
4. Settings:
   - **Name**: `sitepeek-backend`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"
6. **Copy your Render URL** (e.g., `https://sitepeek-backend.onrender.com`)

---

### Step 3️⃣: Deploy Frontend to Vercel

1. **Update script.js** with your backend URL:
   
   Open `frontend/script.js` and change line 4:
   ```javascript
   const API_BASE_URL = window.location.hostname === 'localhost' 
       ? 'http://localhost:8000' 
       : 'https://YOUR-BACKEND-URL-HERE.railway.app'; // Your actual backend URL
   ```

2. **Push changes**:
   ```powershell
   git add .
   git commit -m "Update backend URL for production"
   git push
   ```

3. **Deploy to Vercel**:
   - Go to https://vercel.com/
   - Click "New Project"
   - Import your `SitePeek` GitHub repository
   - Configure:
     - **Framework Preset**: Other
     - **Root Directory**: `./`
     - **Output Directory**: `frontend`
   - Click "Deploy"
   - Wait 30-60 seconds
   - **Done!** Copy your Vercel URL (e.g., `https://sitepeek.vercel.app`)

---

## ✅ You're Live!

Your app is now deployed:
- **Frontend**: `https://sitepeek.vercel.app`
- **Backend**: `https://sitepeek-production.railway.app`
- **API Docs**: `https://sitepeek-production.railway.app/docs`

---

## 🔧 Troubleshooting

### CORS Error?
Update `backend/main.py` line 16 with your actual Vercel URL:
```python
allow_origins=[
    "http://localhost:3000",
    "https://sitepeek.vercel.app",  # Your actual Vercel URL
    "https://*.vercel.app",
],
```
Then push to GitHub - Railway/Render will auto-deploy.

### API Not Working?
- Check backend is running on Railway/Render dashboard
- Verify backend URL in `frontend/script.js` is correct
- Check browser console for errors

---

## 💰 Costs

- **Vercel**: FREE ✅
- **Railway**: $5/month free credit ✅
- **Render**: FREE (but slower on first load) ✅

---

## 📚 Need More Details?

See `DEPLOYMENT.md` for the complete detailed guide!

---

## 🎉 That's It!

Your SitePeek app is now accessible to the world! Share your Vercel URL with anyone!

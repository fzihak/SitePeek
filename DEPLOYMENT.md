# SitePeek Deployment Guide

## 🚀 Deploying to Vercel (Frontend) + Railway/Render (Backend)

### Prerequisites

1. A GitHub account
2. A Vercel account (sign up at https://vercel.com)
3. A Railway account (sign up at https://railway.app) OR Render account (https://render.com)
4. Git installed on your computer

---

## Part 1: Push Your Code to GitHub

### Step 1: Initialize Git Repository

```bash
cd "D:\Self Project\SitePeek"
git init
git add .
git commit -m "Initial commit: SitePeek project"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `SitePeek`
3. Make it Public or Private
4. Don't initialize with README (you already have one)
5. Click "Create repository"

### Step 3: Push to GitHub

```bash
git remote add origin https://github.com/YOUR-USERNAME/SitePeek.git
git branch -M main
git push -u origin main
```

---

## Part 2: Deploy Backend to Railway (Recommended)

### Why Railway?
- Free tier available
- Easy Python deployment
- Auto HTTPS
- Simple environment variables

### Steps:

1. **Go to Railway**: https://railway.app/
2. **Sign in** with GitHub
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your SitePeek repository**
6. **Configure deployment:**
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

7. **Add Environment Variables** (if needed):
   - Click on your service
   - Go to "Variables" tab
   - Add any needed variables

8. **Get your backend URL:**
   - Railway will provide a URL like: `https://sitepeek-backend-production.up.railway.app`
   - Copy this URL

### Alternative: Render.com

1. Go to https://render.com/
2. Click "New" → "Web Service"
3. Connect your GitHub repo
4. Configure:
   - Name: `sitepeek-backend`
   - Root Directory: `backend`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Click "Create Web Service"
6. Copy your backend URL (e.g., `https://sitepeek-backend.onrender.com`)

---

## Part 3: Update Frontend with Backend URL

### Update script.js

Open `frontend/script.js` and update line 4:

```javascript
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://YOUR-ACTUAL-BACKEND-URL.railway.app'; // Replace with your Railway/Render URL
```

**Example:**
```javascript
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://sitepeek-backend-production.up.railway.app';
```

### Commit and push changes:

```bash
git add frontend/script.js
git commit -m "Update API URL for production"
git push
```

---

## Part 4: Deploy Frontend to Vercel

### Steps:

1. **Go to Vercel**: https://vercel.com/
2. **Sign in** with GitHub
3. **Click "Add New..." → "Project"**
4. **Import your SitePeek repository**
5. **Configure project:**
   - Framework Preset: `Other`
   - Root Directory: `./` (leave as default)
   - Build Command: Leave empty
   - Output Directory: `frontend`
   - Install Command: Leave empty

6. **Click "Deploy"**

7. **Wait for deployment** (usually takes 30-60 seconds)

8. **Get your URL:**
   - Vercel will provide a URL like: `https://sitepeek.vercel.app`
   - You can also add a custom domain later

---

## Part 5: Update Backend CORS Settings

### Important: Update CORS in backend/main.py

Open `backend/main.py` and update the CORS settings to allow your Vercel frontend:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://sitepeek.vercel.app",  # Your Vercel URL
        "https://*.vercel.app"  # All Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Commit and push:

```bash
git add backend/main.py
git commit -m "Update CORS for production"
git push
```

Railway/Render will automatically redeploy with the new changes.

---

## Part 6: Test Your Deployment

1. **Visit your Vercel URL**: `https://sitepeek.vercel.app`
2. **Test the analyzer** with a public website like `https://example.com`
3. **Check browser console** for any errors
4. **Verify downloads** work correctly

---

## 🎯 Quick Reference

### Your Deployment URLs:

- **Frontend (Vercel)**: `https://sitepeek.vercel.app`
- **Backend (Railway)**: `https://sitepeek-backend-production.up.railway.app`
- **API Docs**: `https://sitepeek-backend-production.up.railway.app/docs`

### Useful Commands:

```bash
# Check deployment status
vercel --prod

# View logs (Vercel)
vercel logs

# Redeploy frontend
git push  # Vercel auto-deploys on push

# Local development
cd backend && python main.py
cd frontend && python -m http.server 3000
```

---

## 🔧 Troubleshooting

### Issue: CORS Errors

**Solution:** Update `backend/main.py` CORS settings with your Vercel URL

### Issue: API not responding

**Solution:** 
- Check Railway/Render logs
- Verify backend URL in `script.js`
- Ensure backend is running

### Issue: 404 on Vercel

**Solution:** Check `vercel.json` configuration

### Issue: Build fails on Vercel

**Solution:** Ensure `vercel.json` has correct `outputDirectory: "frontend"`

---

## 🌟 Optional: Custom Domain

### On Vercel:
1. Go to your project settings
2. Click "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

### On Railway:
1. Go to your service settings
2. Click "Settings" → "Domains"
3. Add custom domain
4. Update DNS records

---

## 📊 Monitoring

### Railway Dashboard:
- View logs
- Monitor CPU/Memory usage
- Check deployment status

### Vercel Dashboard:
- View analytics
- Monitor bandwidth
- Check deployment logs

---

## 💡 Tips

1. **Use environment variables** for sensitive data
2. **Enable caching** on Vercel for better performance
3. **Monitor usage** to stay within free tier limits
4. **Set up GitHub Actions** for automated testing
5. **Add rate limiting** to your backend API

---

## 🆓 Free Tier Limits

### Vercel:
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Automatic HTTPS
- ✅ CDN included

### Railway:
- ✅ $5 free credit/month
- ✅ Enough for small projects
- ✅ Auto-scaling

### Render:
- ✅ Free tier available
- ⚠️ Spins down after inactivity (may be slow on first request)

---

## 🎉 You're Done!

Your SitePeek application is now live and accessible worldwide!

**Need help?** Check the logs on Railway/Render and Vercel for debugging.

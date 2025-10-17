# 🚀 Quick Deployment Checklist

## Before Deploying:

- [ ] Push code to GitHub
- [ ] Test locally (backend on :8000, frontend on :3000)
- [ ] Check all features work correctly

## Deploy Backend (Railway or Render):

### Railway:
1. [ ] Go to https://railway.app/
2. [ ] New Project → Deploy from GitHub
3. [ ] Select SitePeek repository
4. [ ] Root directory: `backend`
5. [ ] Deploy and copy backend URL

### Render:
1. [ ] Go to https://render.com/
2. [ ] New → Web Service
3. [ ] Connect GitHub repo
4. [ ] Root directory: `backend`
5. [ ] Runtime: Python 3
6. [ ] Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. [ ] Deploy and copy backend URL

## Update Frontend:

1. [ ] Open `frontend/script.js`
2. [ ] Update `API_BASE_URL` with your backend URL:
```javascript
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://YOUR-BACKEND-URL.railway.app';
```
3. [ ] Commit and push changes

## Deploy Frontend (Vercel):

1. [ ] Go to https://vercel.com/
2. [ ] New Project → Import Git Repository
3. [ ] Select SitePeek
4. [ ] Configure:
   - Root Directory: `./`
   - Output Directory: `frontend`
5. [ ] Deploy
6. [ ] Copy Vercel URL

## Final Steps:

1. [ ] Update backend CORS in `backend/main.py` with Vercel URL
2. [ ] Test deployed site
3. [ ] Check all features work
4. [ ] Celebrate! 🎉

---

## Your URLs:

**Frontend (Vercel):** `https://_____________.vercel.app`

**Backend (Railway/Render):** `https://_____________.railway.app`

**API Docs:** `https://_____________.railway.app/docs`

---

## Need Help?

See `DEPLOYMENT.md` for detailed instructions!

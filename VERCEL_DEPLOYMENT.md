# 🚀 FinWise AI – Vercel Monorepo Deployment Guide

**Perfect for hackathons!** Deploy a fullstack app with frontend and backend on **one platform** using Vercel.

Vercel handles:
- ✅ Frontend (React) with auto-rebuilding
- ✅ Backend (FastAPI) as serverless functions
- ✅ Environment variables
- ✅ Git integration (auto-deploy on push)
- ✅ Free SSL/HTTPS
- ✅ $0 cost for your usage level

---

## 0) Prerequisites

- GitHub repo created and pushed (`git remote add origin ...`)
- MongoDB Atlas cluster created (free tier OK)
- Gemini API Key from MakerSuite
- Vercel account (sign up at https://vercel.com with GitHub)

---

## 1) How Vercel Monorepo Works

**Your repo structure:**
```
FinWise-AI/
├── frontend/          → React app (Vercel builds → static site)
├── backend/
│   ├── app/
│   │   ├── main.py    → FastAPI (Vercel → serverless functions)
│   │   ├── agents/
│   │   ├── routes/
│   │   └── ...
│   └── requirements.txt
├── vercel.json        → Configuration (routing, builds, env vars)
└── .vercelignore
```

**Request flow:**
```
User visits: https://finwise-ai.vercel.app

1. GET /
   → Vercel serves frontend/dist/index.html (React app)

2. GET /api/transactions
   → Vercel routes to backend/api/main.py (serverless function)

3. React app calls /api/...
   → Backend handles, connects to MongoDB, returns JSON
```

---

## 2) Files Already Created

✅ `vercel.json` - Routing & build config
✅ `backend/api/main.py` - FastAPI app for serverless
✅ `.vercelignore` - Files to exclude from build

---

## 3) Push to GitHub

Push all changes with the new Vercel config:

```powershell
cd "c:\Users\Aarya\Documents\FinWise AI"
git add .
git commit -m "Add Vercel monorepo config"
git push origin master
```

---

## 4) Deploy on Vercel (UI Method - Easiest)

### Step 1: Go to Vercel
1. Visit https://vercel.com
2. Sign in with GitHub
3. Click "Add New..." → "Project"

### Step 2: Import Repository
1. Click "Import GitHub Repository"
2. Find and select `aarya-16/FinWise-AI`
3. Click "Import"

### Step 3: Configure Project
1. **Project Name:** (auto-filled, e.g., `finwise-ai`)
2. **Framework Preset:** Auto-detected (ignore or set to "Other")
3. **Root Directory:** Leave blank (Vercel detects from `vercel.json`)

### Step 4: Set Environment Variables
Click "Environment Variables" and add these three:

| Key | Value | Example |
|-----|-------|---------|
| `MONGODB_URI` | Your Atlas connection string | `mongodb+srv://user:pass@cluster.mongodb.net/finwise_ai` |
| `MONGODB_DB_NAME` | Database name | `finwise_ai` |
| `GEMINI_API_KEY` | Your Gemini API key | `sk-...` |

Leave `Production`, `Preview`, and `Development` checked for all.

### Step 5: Deploy
Click "Deploy" and wait ~3-5 minutes for:
1. Frontend build (npm install, npm run build)
2. Backend dependency install (pip install)
3. Serverless functions packaging
4. CDN distribution

Once done, you'll get a URL like: `https://finwise-ai.vercel.app`

### Step 6: Verify
Visit your URL:
- `https://finwise-ai.vercel.app` → React app loads
- `https://finwise-ai.vercel.app/api/health` → Returns `{"status": "healthy"}`

---

## 5) Deploy on Vercel (CLI Method - Faster)

If you prefer command-line:

### Install Vercel CLI
```powershell
npm install -g vercel
```

### Login to Vercel
```powershell
vercel login
```

### Deploy
```powershell
cd "c:\Users\Aarya\Documents\FinWise AI"
vercel --prod
```

Follow prompts and done!

---

## 6) Test Your Deployment

### 1. Frontend Loads
```
Visit: https://your-app.vercel.app
Expected: Dashboard with "💰 FinWise AI" title
```

### 2. API Health
```
Visit: https://your-app.vercel.app/api/health
Expected: {"status": "healthy"}
```

### 3. Add Transaction
```
1. Fill transaction form
2. Click "Add Transaction"
3. Expected: Transaction categorized by AI
```

### 4. Upload CSV
```
1. Click file input
2. Select sample_transactions.csv
3. Expected: 15 transactions imported and categorized
```

### 5. View Insights
```
Expected: AI insights banner appears at top
Shows income analysis, spending patterns, recommendations
```

---

## 7) Troubleshooting

### Frontend builds but API returns 500
- Check environment variables are set in Vercel
- Check Vercel deployment logs: Project → Deployments → latest → Logs
- Verify MongoDB connection string (test format in Atlas)

### MongoDB connection fails
- Error in logs: `connection refused` or `auth failed`
- Check IP allowlist in MongoDB Atlas (Settings → Network Access)
- For testing: add `0.0.0.0/0` to allow all IPs
- Verify connection string format: `mongodb+srv://user:pass@host/db`

### API returns 404
- Check `vercel.json` routes are correct
- Verify `backend/api/main.py` exists
- Check function size isn't too large (Vercel limit: ~50MB)

### CORS errors
- Already handled (CORS middleware allows all origins)
- Frontend uses relative `/api` paths (not full URLs)

### Frontend shows but API calls timeout
- Cold start on serverless (first call slower)
- Check MongoDB Atlas responding
- Check GEMINI_API_KEY is valid

---

## 8) Environment Variables in Vercel

### Where to Set
1. Project Settings → Environment Variables
2. OR during initial import (recommended)

### Important Notes
- **Don't put .env file in GitHub** (already in .gitignore)
- Vercel loads vars from project settings during build/runtime
- Changes to vars require redeploy

### Add/Update Variables Later
1. Project Settings → Environment Variables
2. Add/edit/delete as needed
3. Changes take effect on next deploy or auto-redeploy

---

## 9) Auto-Deploy on GitHub Push

Vercel automatically deploys when you push to master:

```powershell
cd "c:\Users\Aarya\Documents\FinWise AI"

# Make code changes
git add .
git commit -m "Fix transaction categorization"
git push origin master

# Vercel automatically starts deployment!
# Check status at: https://vercel.com/dashboard
```

---

## 10) Custom Domain (Optional)

### Add Custom Domain
1. Project Settings → Domains
2. Add your domain (e.g., finwise.ai)
3. Follow DNS setup instructions
4. Free SSL certificate auto-generated

---

## 11) Development vs Production

**Local Dev (npm run dev + uvicorn):**
```
Frontend: http://localhost:5173
Backend: http://localhost:8000
API calls: http://localhost:8000/api
```

**Vercel Production:**
```
Frontend: https://your-app.vercel.app
Backend: serverless at https://your-app.vercel.app/api
API calls: /api (relative, same domain)
```

---

## 12) Common Pitfalls & Solutions

### "Build failed: npm: command not found"
- Vercel should auto-detect Node.js
- Check `frontend/package.json` exists
- Try re-importing project

### "ModuleNotFoundError: No module named 'motor'"
- Python dependencies not installed
- Check `backend/requirements.txt` lists all packages
- Verify it includes:
  - fastapi
  - uvicorn
  - motor
  - pymongo
  - pydantic
  - google-generativeai
  - python-dotenv
  - pandas

### "Cannot find module @vercel/python"
- Vercel auto-detects Python from `backend/requirements.txt`
- Ensure file exists at correct path
- Redeploy after checking file exists

### API slow on first request
- Vercel serverless has cold starts (1-2 sec first request)
- Subsequent requests fast
- Normal behavior, not a bug!

---

## 13) Monitoring & Logs

### View Deployment Logs
1. https://vercel.com/dashboard
2. Click your project
3. "Deployments" tab
4. Click latest deployment
5. "Logs" to see build output

### Real-time Logs
```powershell
# If using Vercel CLI
vercel logs --follow
```

### Check Status
1. https://your-app.vercel.app/api/health
2. Should return `{"status": "healthy"}`

---

## 14) Performance Tips

### Make Cold Starts Faster
1. Remove unused imports from `backend/app/main.py`
2. Keep `requirements.txt` minimal
3. Lazy-load heavy dependencies if possible

### Optimize Frontend
1. Already configured with Vite (fast!)
2. D3.js charts render client-side
3. Consider lazy-loading route components for huge apps

### Database Optimization
- MongoDB Atlas free tier is sufficient for MVP
- Index important fields later if needed

---

## 15) Scaling After Hackathon

Once your app gains users:

1. **Upgrade MongoDB**
   - Start with paid Atlas cluster
   - Better performance, automatic backups

2. **Vercel Pro** (optional)
   - $20/month for higher limits
   - Or stay on free tier if usage is low

3. **Add Caching**
   - Vercel Edge Config for static data
   - Redis for session caching

4. **Analytics**
   - Vercel Web Analytics
   - MongoDB Atlas monitoring

---

## 16) Redeploy After Changes

### Option 1: Auto (Recommended)
```powershell
git push origin master
# Vercel auto-deploys!
```

### Option 2: Manual
```powershell
vercel --prod
# or use Vercel dashboard
```

---

## 17) Rollback to Previous Deployment

If something breaks:

1. https://vercel.com/dashboard
2. Click project → Deployments
3. Find working deployment
4. Click "..." → "Promote to Production"

Done! Instantly reverted.

---

## 18) Cost Breakdown

**Free tier includes:**
- ✅ Unlimited deployments
- ✅ SSL/HTTPS
- ✅ CDN globally
- ✅ Serverless functions: 100GB/month (way more than you'll use)
- ✅ Storage: free

**Total cost for MVP:** **$0** (unless MongoDB Atlas goes over free tier)

---

## 19) Hackathon Demo Checklist

Before presenting:

- [ ] Push final code to GitHub
- [ ] Verify Vercel deployment succeeded
- [ ] Test all features on production URL
- [ ] Upload sample_transactions.csv and verify AI categorization
- [ ] Check AI insights appear
- [ ] Set a goal and verify progress tracking
- [ ] Note URL to share with judges
- [ ] Test on mobile (responsive design)

---

## 20) Quick Reference Commands

```powershell
# Push to GitHub (triggers auto-deploy)
git add .
git commit -m "Message"
git push origin master

# Deploy via CLI
vercel --prod

# Check status
vercel status

# View logs
vercel logs

# Delete project (if needed)
vercel remove
```

---

## 🎉 You're Ready!

Your FinWise AI app is **live on Vercel** with:
- ✅ React frontend
- ✅ FastAPI backend
- ✅ MongoDB integration
- ✅ AI agents (Gemini API)
- ✅ Free SSL/HTTPS
- ✅ Global CDN
- ✅ Auto-deploy on push

**Share your URL:** `https://your-app.vercel.app`

---

## Need Help?

- Vercel Docs: https://vercel.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- MongoDB Atlas: https://docs.atlas.mongodb.com

**Questions about FinWise AI deployment?** Check the logs or reach out!

Good luck with the hackathon! 🚀

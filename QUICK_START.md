# FinWise AI - Quick Start Commands

## Prerequisites Check
- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] MongoDB running
- [ ] Gemini API key obtained

## Backend Setup (PowerShell Terminal 1)

```powershell
# Navigate to backend
cd "c:\Users\Aarya\Documents\FinWise AI\backend"

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# If execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt

# Create .env file (IMPORTANT - DO THIS MANUALLY!)
# Copy .env.example to .env
# Add your Gemini API key

# Start backend server
uvicorn app.main:app --reload
```

**Expected output:**
```
✅ Connected to MongoDB: finwise_ai
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Test it:** http://localhost:8000/health

---

## Frontend Setup (PowerShell Terminal 2)

```powershell
# Navigate to frontend
cd "c:\Users\Aarya\Documents\FinWise AI\frontend"

# Install dependencies
npm install

# Start development server
npm run dev
```

**Expected output:**
```
VITE v5.0.11  ready in 500 ms
➜  Local:   http://localhost:5173/
```

**Open in browser:** http://localhost:5173

---

## Verify Everything Works

```powershell
# In a third terminal, from project root
cd "c:\Users\Aarya\Documents\FinWise AI"
python test_backend.py
```

---

## Quick Test Flow

1. **Open app:** http://localhost:5173
2. **Upload CSV:** Use `sample_transactions.csv`
3. **Check AI categorization:** See categories assigned
4. **View insights:** AI coaching should appear
5. **Add transaction manually:** Test real-time categorization

---

## Stop Servers

**Backend (Terminal 1):**
```
Ctrl + C
```

**Frontend (Terminal 2):**
```
Ctrl + C
```

---

## Restart from Scratch

**Backend:**
```powershell
cd "c:\Users\Aarya\Documents\FinWise AI\backend"
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

**Frontend:**
```powershell
cd "c:\Users\Aarya\Documents\FinWise AI\frontend"
npm run dev
```

---

## Common Commands

### Backend

```powershell
# Install new package
pip install package-name

# Update requirements.txt
pip freeze > requirements.txt

# Check installed packages
pip list
```

### Frontend

```powershell
# Install new package
npm install package-name

# Build for production
npm run build

# Preview production build
npm run preview
```

### MongoDB

```powershell
# Check if MongoDB is running
mongod --version

# Access MongoDB shell (optional)
mongosh
```

---

## Troubleshooting Quick Fixes

### Backend not starting?
```powershell
# Reinstall dependencies
cd backend
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Frontend not starting?
```powershell
# Clear and reinstall
cd frontend
rm -r node_modules
rm package-lock.json
npm install
```

### .env file issues?
```powershell
# Check file exists
cd backend
ls .env

# View contents (check API key is there)
cat .env
```

---

## File Locations

**Backend .env file:**
```
c:\Users\Aarya\Documents\FinWise AI\backend\.env
```

**Sample CSV:**
```
c:\Users\Aarya\Documents\FinWise AI\sample_transactions.csv
```

**Documentation:**
```
c:\Users\Aarya\Documents\FinWise AI\SETUP_GUIDE.md
c:\Users\Aarya\Documents\FinWise AI\HACKATHON_GUIDE.md
c:\Users\Aarya\Documents\FinWise AI\PROJECT_SUMMARY.md
```

---

## API Endpoints Reference

**Base URL:** http://localhost:8000

- `GET /` - Root
- `GET /health` - Health check
- `POST /api/transactions/` - Create transaction
- `GET /api/transactions/` - List transactions
- `POST /api/transactions/bulk` - Upload CSV
- `GET /api/insights/` - Get AI insights
- `POST /api/goals/` - Create goal
- `GET /api/goals/` - List goals

---

## Need Help?

1. Check `SETUP_GUIDE.md` for detailed instructions
2. Check `PROJECT_SUMMARY.md` for architecture overview
3. Check terminal output for error messages
4. Verify all prerequisites are installed
5. Make sure MongoDB is running
6. Verify Gemini API key is set in .env

---

**Ready to demo? You've got this! 🚀**

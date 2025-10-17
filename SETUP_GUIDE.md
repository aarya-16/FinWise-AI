# FinWise AI - Setup Guide

## Quick Start Guide

### Prerequisites

1. **Python 3.8+** - [Download](https://www.python.org/downloads/)
2. **Node.js 16+** - [Download](https://nodejs.org/)
3. **MongoDB** - [Download](https://www.mongodb.com/try/download/community)
4. **Gemini API Key** - [Get it here](https://makersuite.google.com/app/apikey)

---

## Backend Setup (FastAPI + MongoDB)

### Step 1: Navigate to backend directory
```powershell
cd "c:\Users\Aarya\Documents\FinWise AI\backend"
```

### Step 2: Create virtual environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Create .env file
Create a file named `.env` in the backend directory:
```
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=finwise_ai
GEMINI_API_KEY=your_actual_gemini_api_key_here
PORT=8000
```

**IMPORTANT:** Replace `your_actual_gemini_api_key_here` with your real Gemini API key!

### Step 5: Start MongoDB
Make sure MongoDB is running on your system. If installed locally:
```powershell
# MongoDB should be running as a service
# Or start it manually if needed
```

### Step 6: Run the backend
```powershell
uvicorn app.main:app --reload
```

You should see:
```
✅ Connected to MongoDB: finwise_ai
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Test it by visiting: http://localhost:8000/health

---

## Frontend Setup (React + Vite)

Open a **NEW** PowerShell window.

### Step 1: Navigate to frontend directory
```powershell
cd "c:\Users\Aarya\Documents\FinWise AI\frontend"
```

### Step 2: Install dependencies
```powershell
npm install
```

This will install:
- React
- Vite
- D3.js
- Axios
- date-fns

### Step 3: Run the development server
```powershell
npm run dev
```

You should see:
```
  VITE v5.0.11  ready in 500 ms

  ➜  Local:   http://localhost:5173/
```

### Step 4: Open in browser
Visit: http://localhost:5173

---

## Testing the Application

### 1. Add Manual Transaction
- Fill in the form on the left
- Click "Add Transaction"
- AI will automatically categorize it!

### 2. Upload Sample CSV
- Use the provided `sample_transactions.csv` file
- Click "Choose File" and select it
- Watch as 15 transactions are imported and categorized

### 3. View AI Insights
- Once you have 3+ transactions, AI insights will appear
- Get personalized coaching based on your data
- See spending patterns and recommendations

### 4. Set a Goal
- Click "+ New Goal" in the Goals section
- Set a savings target (e.g., ₹10,000)
- Get AI recommendations aligned with your goal

---

## API Endpoints

Once backend is running, you can test these endpoints:

### Health Check
```
GET http://localhost:8000/health
```

### Add Transaction
```
POST http://localhost:8000/api/transactions/
Content-Type: application/json

{
  "date": "2025-10-17T00:00:00",
  "amount": 500,
  "type": "expense",
  "description": "Coffee shop"
}
```

### Get Insights
```
GET http://localhost:8000/api/insights/
```

### Get Transactions
```
GET http://localhost:8000/api/transactions/
```

---

## Demo Flow for Hackathon

1. **Start Fresh**: Show empty dashboard
2. **Upload CSV**: Import sample_transactions.csv (15 transactions)
3. **Show Auto-Categorization**: Highlight AI categories with confidence scores
4. **View Dashboard**: Show interactive D3.js charts
5. **AI Insights**: Display personalized coaching (e.g., "Your income varies by 45%, typical for gig work")
6. **Set Goal**: Create a ₹10,000 emergency fund goal
7. **Get Recommendations**: Show AI suggestions based on income patterns
8. **Add Live Transaction**: Enter a new transaction and watch it categorize in real-time

---

## Troubleshooting

### Backend Issues

**Error: "GEMINI_API_KEY not found"**
- Make sure `.env` file exists in backend directory
- Check that GEMINI_API_KEY is set correctly
- No quotes needed in .env file

**Error: "MongoDB connection failed"**
- Check if MongoDB is running: `mongod --version`
- Try different URI: `mongodb://127.0.0.1:27017`

**Error: "Module not found"**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Frontend Issues

**Error: "Failed to fetch"**
- Make sure backend is running on port 8000
- Check browser console for CORS errors
- Verify proxy settings in vite.config.js

**Charts not showing**
- Need at least 2-3 transactions
- Check browser console for D3.js errors

---

## Project Structure

```
FinWise AI/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── data_analysis_agent.py      # AI categorization
│   │   │   └── behavioral_coaching_agent.py # AI coaching
│   │   ├── models/
│   │   │   └── schemas.py                   # Data models
│   │   ├── routes/
│   │   │   ├── transactions.py              # Transaction API
│   │   │   ├── insights.py                  # Insights API
│   │   │   └── goals.py                     # Goals API
│   │   ├── database.py                      # MongoDB connection
│   │   └── main.py                          # FastAPI app
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── InsightsBanner.jsx
│   │   │   ├── TransactionForm.jsx
│   │   │   ├── TransactionList.jsx
│   │   │   ├── GoalTracker.jsx
│   │   │   ├── SpendingChart.jsx            # D3.js pie chart
│   │   │   └── IncomeExpenseChart.jsx       # D3.js bar chart
│   │   ├── services/
│   │   │   └── api.js                       # Axios API client
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── sample_transactions.csv
└── README.md
```

---

## Key Features to Highlight

✅ **Multi-Agent AI System**
- Data Analysis Agent (categorization)
- Behavioral Coaching Agent (insights & recommendations)

✅ **Real-time AI Processing**
- Transactions categorized as you add them
- Confidence scores displayed

✅ **Proactive Coaching**
- Income volatility analysis
- Spending pattern detection
- Goal-aligned recommendations

✅ **Interactive Visualizations**
- D3.js powered charts
- Real-time updates
- Mobile responsive

✅ **Gig Worker Focused**
- Handles irregular income
- Adapts to income volatility
- Emergency fund recommendations

---

## Getting Your Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key
5. Paste it in backend/.env file

---

## Next Steps After MVP

- Add user authentication
- Implement push notifications
- Add more chart types
- Support multiple users
- Mobile app (React Native)
- Bank API integrations
- SMS parsing for UPI transactions

---

## Support

If you encounter any issues:
1. Check this guide carefully
2. Verify all prerequisites are installed
3. Check that both servers are running
4. Look at terminal output for errors

---

Good luck with your hackathon! 🚀

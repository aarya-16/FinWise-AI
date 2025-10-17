# FinWise AI - MVP

Hyper-personalized financial coaching platform for gig workers using AI agents.

## Tech Stack

**Frontend:**
- React + Vite
- D3.js for visualizations
- Axios for API calls

**Backend:**
- Python FastAPI
- MongoDB
- Google Gemini API for AI agents

## Project Structure

```
finwise-ai/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── agents/    # AI agent logic
│   │   ├── models/    # Pydantic models
│   │   ├── routes/    # API endpoints
│   │   ├── services/  # Business logic
│   │   └── main.py    # FastAPI app
│   ├── requirements.txt
│   └── .env.example
├── frontend/          # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── services/
│   │   ├── utils/
│   │   └── App.jsx
│   └── package.json
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with:
```
MONGODB_URI=mongodb://localhost:27017
GEMINI_API_KEY=your_gemini_api_key_here
```

5. Run the server:
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```

## Features

- ✅ Manual transaction entry & CSV upload
- ✅ AI-powered transaction categorization
- ✅ Behavioral pattern analysis
- ✅ Proactive coaching insights
- ✅ Interactive visualizations
- ✅ Savings goal tracking

## Demo Flow

1. Enter sample gig worker transactions
2. Watch AI categorize automatically
3. View spending patterns and insights
4. Set savings goals
5. Get personalized coaching recommendations

## API Endpoints

- `POST /api/transactions` - Add transaction
- `GET /api/transactions` - Get all transactions
- `POST /api/transactions/bulk` - Upload CSV
- `GET /api/insights` - Get AI-generated insights
- `POST /api/goals` - Set savings goal
- `GET /api/goals` - Get goals

## License

MIT

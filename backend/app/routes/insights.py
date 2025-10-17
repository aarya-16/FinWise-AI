from fastapi import APIRouter, HTTPException
from app.models.schemas import InsightResponse
from app.database import get_database
from app.agents.behavioral_coaching_agent import BehavioralCoachingAgent
from datetime import datetime

router = APIRouter()
coaching_agent = BehavioralCoachingAgent()

@router.get("/", response_model=InsightResponse)
async def get_insights():
    """Get AI-generated financial insights and coaching"""
    db = get_database()
    
    # Get recent transactions
    cursor = db.transactions.find({"user_id": "default_user"}).sort("date", -1).limit(100)
    transactions = await cursor.to_list(length=100)
    
    if not transactions:
        raise HTTPException(
            status_code=404, 
            detail="No transactions found. Add some transactions first to get insights."
        )
    
    # Get user goals
    goals_cursor = db.goals.find({"user_id": "default_user", "status": "active"})
    goals = await goals_cursor.to_list(length=10)
    
    # Generate insights using AI
    result = await coaching_agent.analyze_and_coach(transactions, goals)
    
    return InsightResponse(
        insights=result["insights"],
        recommendations=result["recommendations"],
        income_analysis=result["income_analysis"],
        expense_analysis=result["expense_analysis"],
        generated_at=datetime.utcnow()
    )

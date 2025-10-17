from fastapi import APIRouter, HTTPException
from app.models.schemas import GoalCreate, Goal
from app.database import get_database
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/", response_model=dict)
async def create_goal(goal: GoalCreate):
    """Create a new savings goal"""
    db = get_database()
    
    # Prepare goal document
    goal_dict = goal.model_dump()
    goal_dict["user_id"] = "default_user"
    goal_dict["created_at"] = datetime.utcnow()
    goal_dict["status"] = "active"
    
    # Insert into database
    result = await db.goals.insert_one(goal_dict)
    goal_dict["_id"] = str(result.inserted_id)
    
    return {
        "message": "Goal created successfully",
        "goal": goal_dict
    }

@router.get("/")
async def get_goals():
    """Get all goals for the user"""
    db = get_database()
    
    cursor = db.goals.find({"user_id": "default_user"}).sort("created_at", -1)
    goals = await cursor.to_list(length=100)
    
    # Convert ObjectId to string
    for goal in goals:
        goal["_id"] = str(goal["_id"])
    
    return {
        "goals": goals,
        "count": len(goals)
    }

@router.patch("/{goal_id}")
async def update_goal(goal_id: str, current_amount: float = None, status: str = None):
    """Update goal progress or status"""
    db = get_database()
    
    update_data = {}
    if current_amount is not None:
        update_data["current_amount"] = current_amount
    if status is not None:
        update_data["status"] = status
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    
    try:
        result = await db.goals.update_one(
            {"_id": ObjectId(goal_id), "user_id": "default_user"},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        return {"message": "Goal updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{goal_id}")
async def delete_goal(goal_id: str):
    """Delete a goal"""
    db = get_database()
    
    try:
        result = await db.goals.delete_one({
            "_id": ObjectId(goal_id),
            "user_id": "default_user"
        })
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Goal not found")
        
        return {"message": "Goal deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

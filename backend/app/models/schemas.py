from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class TransactionBase(BaseModel):
    date: datetime
    amount: float
    type: Literal["income", "expense"]
    description: str
    category: Optional[str] = None
    confidence_score: Optional[float] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str = "default_user"  # Simplified for MVP
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class GoalBase(BaseModel):
    title: str
    target_amount: float
    target_date: datetime
    current_amount: float = 0.0

class GoalCreate(GoalBase):
    pass

class Goal(GoalBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str = "default_user"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "active"

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class InsightResponse(BaseModel):
    insights: list[str]
    recommendations: list[str]
    income_analysis: dict
    expense_analysis: dict
    generated_at: datetime = Field(default_factory=datetime.utcnow)

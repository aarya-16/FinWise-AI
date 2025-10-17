from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.schemas import TransactionCreate, Transaction
from app.database import get_database
from app.agents.data_analysis_agent import DataAnalysisAgent
from datetime import datetime
from bson import ObjectId
import csv
import io

router = APIRouter()
data_agent = DataAnalysisAgent()

@router.post("/", response_model=dict)
async def create_transaction(transaction: TransactionCreate):
    """Create a new transaction with AI categorization"""
    db = get_database()
    
    # Get AI categorization
    categorization = await data_agent.categorize_transaction(
        description=transaction.description,
        amount=transaction.amount,
        transaction_type=transaction.type
    )
    
    # Prepare transaction document
    transaction_dict = transaction.model_dump()
    transaction_dict["category"] = categorization["category"]
    transaction_dict["confidence_score"] = categorization["confidence_score"]
    transaction_dict["user_id"] = "default_user"
    transaction_dict["created_at"] = datetime.utcnow()
    
    # Insert into database
    result = await db.transactions.insert_one(transaction_dict)
    transaction_dict["_id"] = str(result.inserted_id)
    
    return {
        "message": "Transaction created successfully",
        "transaction": transaction_dict
    }

@router.get("/")
async def get_transactions(limit: int = 100, skip: int = 0):
    """Get all transactions for the user"""
    db = get_database()
    
    cursor = db.transactions.find({"user_id": "default_user"}).sort("date", -1).skip(skip).limit(limit)
    transactions = await cursor.to_list(length=limit)
    
    # Convert ObjectId to string
    for txn in transactions:
        txn["_id"] = str(txn["_id"])
    
    return {
        "transactions": transactions,
        "count": len(transactions)
    }

@router.post("/bulk")
async def upload_transactions_csv(file: UploadFile = File(...)):
    """Upload transactions via CSV file"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    db = get_database()
    
    # Read CSV content
    contents = await file.read()
    csv_data = contents.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(csv_data))
    
    transactions_added = []
    errors = []
    
    for row_num, row in enumerate(csv_reader, start=2):
        try:
            # Parse row (expected columns: date, amount, type, description)
            date_str = row.get('date', '').strip()
            amount = float(row.get('amount', 0))
            txn_type = row.get('type', '').strip().lower()
            description = row.get('description', '').strip()
            
            # Validate
            if not date_str or not amount or txn_type not in ['income', 'expense'] or not description:
                errors.append(f"Row {row_num}: Invalid or missing data")
                continue
            
            # Parse date
            try:
                date = datetime.fromisoformat(date_str)
            except:
                try:
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                except:
                    errors.append(f"Row {row_num}: Invalid date format")
                    continue
            
            # Get AI categorization
            categorization = await data_agent.categorize_transaction(
                description=description,
                amount=amount,
                transaction_type=txn_type
            )
            
            # Create transaction document
            transaction_dict = {
                "date": date,
                "amount": amount,
                "type": txn_type,
                "description": description,
                "category": categorization["category"],
                "confidence_score": categorization["confidence_score"],
                "user_id": "default_user",
                "created_at": datetime.utcnow()
            }
            
            # Insert into database
            result = await db.transactions.insert_one(transaction_dict)
            transaction_dict["_id"] = str(result.inserted_id)
            transactions_added.append(transaction_dict)
        
        except Exception as e:
            errors.append(f"Row {row_num}: {str(e)}")
    
    return {
        "message": f"Processed {len(transactions_added)} transactions",
        "transactions_added": len(transactions_added),
        "errors": errors
    }

@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: str):
    """Delete a transaction"""
    db = get_database()
    
    try:
        result = await db.transactions.delete_one({
            "_id": ObjectId(transaction_id),
            "user_id": "default_user"
        })
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        return {"message": "Transaction deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

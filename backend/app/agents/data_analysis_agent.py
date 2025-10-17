import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()

class DataAnalysisAgent:
    """Agent responsible for categorizing transactions using Gemini AI"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def categorize_transaction(self, description: str, amount: float, transaction_type: str) -> dict:
        """
        Categorize a transaction using Gemini AI
        
        Returns:
            dict: {
                "category": str,
                "confidence_score": float (0-1)
            }
        """
        
        prompt = f"""
You are a financial transaction categorization expert. Analyze this transaction and categorize it.

Transaction Details:
- Description: {description}
- Amount: ₹{amount}
- Type: {transaction_type}

Categories for expenses: Food & Dining, Transportation, Bills & Utilities, Shopping, Entertainment, Healthcare, Education, Other Expense
Categories for income: Freelance/Gig Income, Salary, Business Income, Investment Returns, Other Income

Respond with ONLY a JSON object in this exact format:
{{
    "category": "category name",
    "confidence_score": 0.95,
    "reasoning": "brief explanation"
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Extract JSON from markdown code blocks if present
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            result = json.loads(result_text)
            
            return {
                "category": result.get("category", "Uncategorized"),
                "confidence_score": result.get("confidence_score", 0.7)
            }
        
        except Exception as e:
            print(f"Error in categorization: {str(e)}")
            # Fallback to simple rule-based categorization
            return self._fallback_categorization(description, transaction_type)
    
    def _fallback_categorization(self, description: str, transaction_type: str) -> dict:
        """Simple rule-based fallback categorization"""
        description_lower = description.lower()
        
        if transaction_type == "income":
            if any(word in description_lower for word in ["freelance", "gig", "project", "client"]):
                return {"category": "Freelance/Gig Income", "confidence_score": 0.6}
            elif any(word in description_lower for word in ["salary", "wage"]):
                return {"category": "Salary", "confidence_score": 0.6}
            else:
                return {"category": "Other Income", "confidence_score": 0.5}
        
        else:  # expense
            if any(word in description_lower for word in ["food", "restaurant", "meal", "swiggy", "zomato"]):
                return {"category": "Food & Dining", "confidence_score": 0.6}
            elif any(word in description_lower for word in ["uber", "ola", "transport", "petrol", "fuel"]):
                return {"category": "Transportation", "confidence_score": 0.6}
            elif any(word in description_lower for word in ["electricity", "water", "rent", "bill"]):
                return {"category": "Bills & Utilities", "confidence_score": 0.6}
            elif any(word in description_lower for word in ["amazon", "flipkart", "shopping", "clothes"]):
                return {"category": "Shopping", "confidence_score": 0.6}
            else:
                return {"category": "Other Expense", "confidence_score": 0.5}

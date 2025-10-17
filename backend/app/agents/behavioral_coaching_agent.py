import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json

load_dotenv()

class BehavioralCoachingAgent:
    """Agent responsible for analyzing financial behavior and providing coaching"""
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def analyze_and_coach(self, transactions: list, goals: list = None) -> dict:
        """
        Analyze financial behavior and generate personalized coaching
        
        Args:
            transactions: List of transaction documents
            goals: List of user goals
            
        Returns:
            dict with insights, recommendations, and analysis
        """
        
        # Prepare transaction summary
        analysis = self._prepare_analysis(transactions)
        
        # Generate AI insights
        ai_insights = await self._generate_insights(analysis, goals)
        
        return {
            "insights": ai_insights.get("insights", []),
            "recommendations": ai_insights.get("recommendations", []),
            "income_analysis": analysis["income_analysis"],
            "expense_analysis": analysis["expense_analysis"]
        }
    
    def _prepare_analysis(self, transactions: list) -> dict:
        """Prepare structured analysis from transactions"""
        
        income_total = 0
        expense_total = 0
        income_by_category = {}
        expense_by_category = {}
        income_transactions = []
        expense_transactions = []
        
        for txn in transactions:
            amount = txn.get("amount", 0)
            category = txn.get("category", "Uncategorized")
            txn_type = txn.get("type")
            
            if txn_type == "income":
                income_total += amount
                income_by_category[category] = income_by_category.get(category, 0) + amount
                income_transactions.append(txn)
            else:
                expense_total += amount
                expense_by_category[category] = expense_by_category.get(category, 0) + amount
                expense_transactions.append(txn)
        
        # Calculate income volatility (coefficient of variation)
        if len(income_transactions) > 1:
            income_amounts = [t.get("amount", 0) for t in income_transactions]
            avg_income = sum(income_amounts) / len(income_amounts)
            variance = sum((x - avg_income) ** 2 for x in income_amounts) / len(income_amounts)
            std_dev = variance ** 0.5
            volatility = (std_dev / avg_income * 100) if avg_income > 0 else 0
        else:
            volatility = 0
        
        return {
            "income_analysis": {
                "total": income_total,
                "by_category": income_by_category,
                "count": len(income_transactions),
                "volatility": round(volatility, 2)
            },
            "expense_analysis": {
                "total": expense_total,
                "by_category": expense_by_category,
                "count": len(expense_transactions),
                "top_categories": sorted(
                    expense_by_category.items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:3]
            },
            "net_savings": income_total - expense_total,
            "savings_rate": ((income_total - expense_total) / income_total * 100) if income_total > 0 else 0
        }
    
    async def _generate_insights(self, analysis: dict, goals: list = None) -> dict:
        """Generate AI-powered insights and recommendations"""
        
        goal_info = ""
        if goals and len(goals) > 0:
            goal = goals[0]
            goal_info = f"\nUser Goal: Save ₹{goal.get('target_amount', 0)} by {goal.get('target_date', 'N/A')}"
        
        prompt = f"""
You are a financial coach specialized in helping gig workers and informal sector workers manage irregular income.

Financial Summary:
- Total Income: ₹{analysis['income_analysis']['total']:.2f}
- Total Expenses: ₹{analysis['expense_analysis']['total']:.2f}
- Net Savings: ₹{analysis['net_savings']:.2f}
- Savings Rate: {analysis['savings_rate']:.1f}%
- Income Volatility: {analysis['income_analysis']['volatility']:.1f}%
- Number of Income Transactions: {analysis['income_analysis']['count']}
- Number of Expense Transactions: {analysis['expense_analysis']['count']}

Income by Category:
{json.dumps(analysis['income_analysis']['by_category'], indent=2)}

Top Expense Categories:
{json.dumps(dict(analysis['expense_analysis']['top_categories']), indent=2)}
{goal_info}

Provide:
1. 2-3 key insights about their financial behavior (be specific with numbers)
2. 2-3 actionable recommendations tailored to gig workers with irregular income

Respond with ONLY a JSON object in this format:
{{
    "insights": [
        "Your income shows X% volatility, which is typical for gig work...",
        "You're spending Y% of income on Z category..."
    ],
    "recommendations": [
        "Build an emergency fund of ₹X to cover income gaps...",
        "Consider setting aside 20% of each gig payment..."
    ]
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
                "insights": result.get("insights", []),
                "recommendations": result.get("recommendations", [])
            }
        
        except Exception as e:
            print(f"Error generating insights: {str(e)}")
            return self._fallback_insights(analysis)
    
    def _fallback_insights(self, analysis: dict) -> dict:
        """Fallback insights if AI fails"""
        insights = []
        recommendations = []
        
        savings_rate = analysis['savings_rate']
        net_savings = analysis['net_savings']
        
        if savings_rate > 20:
            insights.append(f"Great job! You're saving {savings_rate:.1f}% of your income.")
        elif savings_rate > 0:
            insights.append(f"You're saving {savings_rate:.1f}% of your income. Let's work on increasing this!")
        else:
            insights.append(f"Your expenses exceed income by ₹{abs(net_savings):.2f}. Let's create a plan.")
        
        if analysis['income_analysis']['volatility'] > 30:
            insights.append(f"Your income varies by {analysis['income_analysis']['volatility']:.0f}%, typical for gig work.")
            recommendations.append("Build an emergency fund equal to 2-3 months of expenses to handle income gaps.")
        
        if len(analysis['expense_analysis']['top_categories']) > 0:
            top_category, top_amount = analysis['expense_analysis']['top_categories'][0]
            insights.append(f"Your highest expense is {top_category} at ₹{top_amount:.2f}.")
            recommendations.append(f"Review your {top_category} spending for potential savings opportunities.")
        
        if savings_rate < 20:
            recommendations.append("Try the 50-30-20 rule: 50% needs, 30% wants, 20% savings.")
        
        return {
            "insights": insights[:3],
            "recommendations": recommendations[:3]
        }

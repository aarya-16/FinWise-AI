"""
Simple test script to verify FinWise AI backend setup
Run this after starting the backend server to check if everything works
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✅ Health check passed")
        return True
    else:
        print(f"❌ Health check failed: {response.status_code}")
        return False

def test_root():
    """Test root endpoint"""
    print("\nTesting root endpoint...")
    response = requests.get(f"{BASE_URL}/")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Root endpoint passed: {data['message']}")
        return True
    else:
        print(f"❌ Root endpoint failed: {response.status_code}")
        return False

def test_create_transaction():
    """Test creating a transaction"""
    print("\nTesting transaction creation...")
    transaction_data = {
        "date": datetime.now().isoformat(),
        "amount": 500,
        "type": "expense",
        "description": "Test coffee shop purchase"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/transactions/",
        json=transaction_data
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Transaction created successfully")
        print(f"   Category: {data['transaction']['category']}")
        print(f"   Confidence: {data['transaction']['confidence_score']:.2f}")
        return True
    else:
        print(f"❌ Transaction creation failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

def test_get_transactions():
    """Test getting transactions"""
    print("\nTesting get transactions...")
    response = requests.get(f"{BASE_URL}/api/transactions/")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {data['count']} transactions")
        return True
    else:
        print(f"❌ Get transactions failed: {response.status_code}")
        return False

def test_get_insights():
    """Test getting insights"""
    print("\nTesting AI insights...")
    response = requests.get(f"{BASE_URL}/api/insights/")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ AI insights generated")
        if data.get('insights'):
            print(f"   Found {len(data['insights'])} insights")
            print(f"   Found {len(data['recommendations'])} recommendations")
        return True
    elif response.status_code == 404:
        print("⚠️  No transactions yet - add some first!")
        return True
    else:
        print(f"❌ Get insights failed: {response.status_code}")
        print(f"   Error: {response.text}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("FinWise AI Backend Test Suite")
    print("=" * 50)
    
    tests = [
        test_health,
        test_root,
        test_create_transaction,
        test_get_transactions,
        test_get_insights,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    if failed == 0:
        print("\n🎉 All tests passed! Your backend is ready!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        print("\nCommon issues:")
        print("1. Make sure backend server is running (uvicorn app.main:app --reload)")
        print("2. Check if MongoDB is running")
        print("3. Verify GEMINI_API_KEY is set in .env file")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend server!")
        print("Make sure the backend is running on http://localhost:8000")
        print("\nTo start the backend:")
        print("1. cd backend")
        print("2. Activate venv: .\\venv\\Scripts\\Activate.ps1")
        print("3. Run: uvicorn app.main:app --reload")

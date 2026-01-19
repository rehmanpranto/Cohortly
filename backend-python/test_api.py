"""
Test script to verify API endpoints
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_root():
    """Test root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print(f"✅ Root endpoint: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/api/v1/health")
    print(f"✅ Health endpoint: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    print()

def test_register():
    """Test user registration"""
    data = {
        "email": "student@cohortly.com",
        "password": "student123",
        "full_name": "Student User",
        "phone": "1234567890",
        "role": "STUDENT"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=data)
        print(f"Registration response: {response.status_code}")
        
        if response.status_code == 201:
            print("✅ User registered successfully!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    print()

def test_login():
    """Test user login"""
    data = {
        "email": "student@cohortly.com",
        "password": "student123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=data)
        print(f"Login response: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Login successful!")
            result = response.json()
            print(f"Access Token: {result['access_token'][:50]}...")
            print(f"User: {result['user']['email']}")
            return result['access_token']
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    print()
    return None

if __name__ == "__main__":
    print("🧪 Testing Cohortly API\n")
    print("="*50)
    
    test_root()
    test_health()
    test_register()
    test_login()
    
    print("="*50)
    print("✅ All basic tests completed!")

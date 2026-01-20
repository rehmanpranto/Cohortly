"""
API Test Script
Tests all endpoints to verify the backend is working correctly
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_root():
    """Test root endpoint"""
    print("\n1️⃣  Testing Root Endpoint (GET /)")
    print("-" * 50)
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_health():
    """Test health endpoint"""
    print("\n2️⃣  Testing Health Endpoint (GET /api/v1/health)")
    print("-" * 50)
    response = requests.get(f"{BASE_URL}/api/v1/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200

def test_register():
    """Test user registration"""
    print("\n3️⃣  Testing User Registration (POST /api/v1/auth/register)")
    print("-" * 50)
    
    data = {
        "email": "admin@cohortly.com",
        "password": "admin123",
        "full_name": "Admin User",
        "phone": "1234567890",
        "role": "ADMIN"
    }
    
    print(f"Payload: {json.dumps(data, indent=2)}")
    response = requests.post(f"{BASE_URL}/api/v1/auth/register", json=data)
    print(f"Status: {response.status_code}")
    
    try:
        response_data = response.json()
        print(f"Response: {json.dumps(response_data, indent=2)}")
        if response.status_code == 201:
            return response_data
    except:
        print(f"Response Text: {response.text}")
    
    return None

def test_login(email, password):
    """Test user login"""
    print("\n4️⃣  Testing User Login (POST /api/v1/auth/login)")
    print("-" * 50)
    
    data = {
        "email": email,
        "password": password
    }
    
    print(f"Payload: {json.dumps(data, indent=2)}")
    response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=data)
    print(f"Status: {response.status_code}")
    
    try:
        response_data = response.json()
        print(f"Response: {json.dumps(response_data, indent=2)}")
        if response.status_code == 200:
            return response_data
    except:
        print(f"Response Text: {response.text}")
    
    return None

def main():
    """Run all tests"""
    print("\n" + "=" * 50)
    print("🧪 COHORTLY API TEST SUITE")
    print("=" * 50)
    
    # Test basic endpoints
    root_ok = test_root()
    health_ok = test_health()
    
    # Test authentication flow
    user_data = test_register()
    
    if user_data:
        print("\n✅ Registration successful!")
        # Try to login
        login_data = test_login("admin@cohortly.com", "admin123")
        
        if login_data:
            print("\n✅ Login successful!")
            print(f"\n🔑 Access Token: {login_data['access_token'][:50]}...")
        else:
            print("\n❌ Login failed")
    else:
        print("\n⚠️  Registration failed - checking if user already exists")
        # Try login anyway
        login_data = test_login("admin@cohortly.com", "admin123")
        if login_data:
            print("\n✅ User already exists and login successful!")
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    print(f"✓ Root endpoint: {'PASS' if root_ok else 'FAIL'}")
    print(f"✓ Health endpoint: {'PASS' if health_ok else 'FAIL'}")
    print(f"✓ Authentication: {'PASS' if user_data or login_data else 'FAIL'}")
    print("=" * 50)

if __name__ == "__main__":
    import time
    print("\n⏳ Waiting 3 seconds for server to start...")
    time.sleep(3)
    main()

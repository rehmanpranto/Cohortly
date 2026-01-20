"""
Simple test to debug registration issue
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_registration():
    """Test user registration with detailed error output"""
    print("🧪 Testing User Registration")
    print("=" * 50)
    
    # Test data
    data = {
        "email": "test@cohortly.com",
        "password": "test123456",
        "full_name": "Test User",
        "phone": "1234567890",
        "role": "STUDENT"
    }
    
    print(f"\n📤 Sending POST request to: {BASE_URL}/api/v1/auth/register")
    print(f"📦 Data: {json.dumps(data, indent=2)}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/auth/register",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\n📥 Response Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        try:
            response_data = response.json()
            print(f"📋 Response Body: {json.dumps(response_data, indent=2)}")
        except:
            print(f"📋 Response Body (text): {response.text}")
        
        if response.status_code == 201:
            print("\n✅ Registration successful!")
            return True
        else:
            print(f"\n❌ Registration failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_registration()

"""Test login with debug"""
import requests

url = 'http://127.0.0.1:5000/login'

# First, get the login page to get CSRF token
session = requests.Session()
response = session.get(url)

print(f"GET {url}")
print(f"Status: {response.status_code}")

# Extract CSRF token
from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')
csrf_token = soup.find('input', {'name': 'csrf_token'})

if csrf_token:
    csrf_value = csrf_token.get('value')
    print(f"CSRF Token: {csrf_value[:20]}...")
    
    # Now try to login
    login_data = {
        'email': 'admin@cohortly.com',
        'password': 'Admin@123',
        'remember': 'y',
        'csrf_token': csrf_value
    }
    
    print(f"\nPOST {url}")
    print(f"Data: email={login_data['email']}, password=***")
    
    response = session.post(url, data=login_data, allow_redirects=False)
    
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    
    if response.status_code == 302:
        print(f"\n✅ Login successful! Redirecting to: {response.headers.get('Location')}")
    else:
        print(f"\n❌ Login failed! Response:")
        if 'Invalid email or password' in response.text:
            print("   Error: Invalid email or password")
        else:
            print(f"   Page returned (check form errors)")
else:
    print("❌ Could not find CSRF token!")

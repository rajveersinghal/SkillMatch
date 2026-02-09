import requests
import uuid
import sys

BASE_URL = "http://localhost:8000"

def test_authentication_flow():
    # Use a unique email for each test run to avoid "Email already registered" errors
    unique_id = str(uuid.uuid4())[:8]
    test_email = f"test_{unique_id}@example.com"
    test_password = "securepassword123"
    
    print(f"\n--- Testing Authentication Flow for: {test_email} ---")
    
    # 1. Test Registration
    print("\n1. Testing Registration...")
    reg_response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"email": test_email, "password": test_password}
    )
    
    if reg_response.status_code == 200:
        print("✅ Registration Successful!")
        print(f"   Response: {reg_response.json()}")
    else:
        print(f"❌ Registration Failed (Status {reg_response.status_code})")
        print(f"   Error: {reg_response.text}")
        return # Stop if registration fails

    # 2. Test Registration (Duplicate)
    print("\n2. Testing Duplicate Registration (Expect Failure)...")
    dup_response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"email": test_email, "password": test_password}
    )
    if dup_response.status_code == 400:
        print("✅ Duplicate Detection Successful (Received 400 as expected)")
    else:
        print(f"❌ Unexpected Status for Duplicate: {dup_response.status_code}")

    # 3. Test Login
    print("\n3. Testing Login...")
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": test_email, "password": test_password} # Form data
    )
    
    if login_response.status_code == 200:
        login_data = login_response.json()
        print("✅ Login Successful!")
        print(f"   Access Token: {login_data['access_token'][:15]}...")
        token = login_data['access_token']
    else:
        print(f"❌ Login Failed (Status {login_response.status_code})")
        print(f"   Error: {login_response.text}")
        return

    # 4. Test Login (Invalid Password)
    print("\n4. Testing Login with Wrong Password (Expect Failure)...")
    wrong_login = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": test_email, "password": "wrongpassword"}
    )
    if wrong_login.status_code == 401:
        print("✅ Wrong Password Handled Correctly (Received 401)")
    else:
        print(f"❌ Unexpected Status for Wrong Password: {wrong_login.status_code}")

    print("\n--- Authentication Testing Complete ---")

if __name__ == "__main__":
    try:
        # Check if server is running first
        requests.get(f"{BASE_URL}/health", timeout=2)
        test_authentication_flow()
    except requests.exceptions.ConnectionError:
        print("❌ Error: FastAPI server is not running on http://localhost:8000")
        print("   Please start it with: python -m uvicorn backend.main:app --reload")
        sys.exit(1)

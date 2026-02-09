import requests

BASE_URL = "http://localhost:8000"

def test_health():
    try:
        r = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {r.status_code}")
        print(f"Body: {r.text}")
    except Exception as e:
        print(f"Health check failed: {e}")

def test_login():
    try:
        r = requests.post(f"{BASE_URL}/auth/login", data={"username": "test@example.com", "password": "password"})
        print(f"Login check: {r.status_code}")
        print(f"Body: {r.text}")
    except Exception as e:
        print(f"Login check failed: {e}")

if __name__ == "__main__":
    test_health()
    test_login()

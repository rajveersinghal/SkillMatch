from core.database import get_user_collection
from core.auth import register_user, login_user

import streamlit as st

# Mock secrets if running standalone (or rely on secrets.toml if streamlit is set up correctly, 
# but here we might need to load secrets manually if not running via streamlit run)
# Actually, database.py uses st.secrets. 
# If we run this as a python script, st.secrets won't be populated unless we use streamlit run or mock it.
# Easier to run this via `streamlit run tests/test_auth_backend.py` inside the app?
# Or just mock st.secrets.

import toml
try:
    secrets = toml.load(".streamlit/secrets.toml")
    # Monkey patch st.secrets
    st.secrets = secrets
except Exception as e:
    print(f"Could not load secrets: {e}")

def test_auth_flow():
    print("Starting Auth Backend Test...")
    users = get_user_collection()
    test_email = "autotest@example.com"
    test_pass = "securepass123"

    # 1. Cleanup
    users.delete_one({"email": test_email})
    print("Cleaned up old test user.")

    # 2. Register
    assert register_user(test_email, test_pass) == True, "Registration failed"
    print("Registration successful.")

    # 3. Verify in DB
    user = users.find_one({"email": test_email})
    assert user is not None, "User not found in DB"
    assert user["email"] == test_email
    assert user["password"] != test_pass, "Password not hashed!"
    print("User found in DB and password hashed.")

    # 4. Login Success
    assert login_user(test_email, test_pass) == True, "Login with correct password failed"
    print("Login with correct password successful.")

    # 5. Login Failure
    assert login_user(test_email, "wrongpass") == False, "Login with wrong password should fail"
    print("Login with wrong password correctly failed.")

    # 6. Duplicate Register
    assert register_user(test_email, "newpass") == False, "Duplicate registration should fail"
    print("Duplicate registration correctly failed.")

    # 7. Cleanup
    users.delete_one({"email": test_email})
    print("Test Complete & Cleaned up. ✅")

if __name__ == "__main__":
    test_auth_flow()

import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Mock streamlit before importing app modules potentially
sys.modules["streamlit"] = MagicMock()
import streamlit as st
st.secrets = {"MONGO_URI": "mongodb://mock"}

# Mock pymongo
sys.modules["pymongo"] = MagicMock()

# Now we can import auth
# But auth imports database which imports pymongo. 
# We need to ensure database.get_user_collection returns our mock.

# We will patch auth.users_col directly.
# We will patch auth.users_col directly.
import core.auth as auth
from core.auth import register_user, login_user


class MockCollection:
    def __init__(self):
        self.data = []
    
    def find_one(self, query):
        # Simple query support for {"email": ...}
        for doc in self.data:
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                return doc
        return None
    
    def insert_one(self, doc):
        self.data.append(doc)
        return MagicMock(inserted_id="mock_id")

class TestAuth(unittest.TestCase):
    def setUp(self):
        # Reset the mock collection before each test
        self.mock_col = MockCollection()
        auth.users_col = self.mock_col

    def test_register_success(self):
        result = register_user("test@example.com", "password123")
        self.assertTrue(result)
        self.assertEqual(len(self.mock_col.data), 1)
        self.assertEqual(self.mock_col.data[0]["email"], "test@example.com")
        # Check password is hashed (not plain)
        self.assertNotEqual(self.mock_col.data[0]["password"], "password123")

    def test_register_duplicate(self):
        register_user("test@example.com", "password123")
        result = register_user("test@example.com", "newpass")
        self.assertFalse(result)
        self.assertEqual(len(self.mock_col.data), 1)

    def test_login_success(self):
        register_user("test@example.com", "password123")
        result = login_user("test@example.com", "password123")
        self.assertTrue(result)

    def test_login_wrong_password(self):
        register_user("test@example.com", "password123")
        result = login_user("test@example.com", "wrongpass")
        self.assertFalse(result)

    def test_login_nonexistent(self):
        result = login_user("nonexistent@example.com", "password123")
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Global variables for lazy initialization
_client = None
_db = None

def get_client():
    global _client
    if _client is None:
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            # We don't raise here to allow non-DB routes to work
            return None
        _client = MongoClient(mongo_uri)
    return _client

def get_db():
    global _db
    if _db is None:
        client = get_client()
        if client:
            _db = client["skillmatch"]
    return _db

def get_user_collection():
    db = get_db()
    if db is None:
        # Instead of raising, we return None and handle it in the router
        return None
    return db["users"]

def get_document_collection():
    db = get_db()
    if db is None:
        # Instead of raising, we return None and handle it in the router
        return None
    return db["documents"]

def check_db_connection():
    try:
        mongo_uri = os.getenv("MONGO_URI")
        if not mongo_uri:
            print("Database Error: MONGO_URI is not set in environment variables.")
            return False
            
        client = get_client()
        if not client:
            return False
            
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        return True
    except Exception as e:
        print(f"Database Connection Exception: {str(e)}")
        return False

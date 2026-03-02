from pymongo import MongoClient
import os
import certifi
from dotenv import load_dotenv

load_dotenv()

# Global variables for lazy initialization
_client = None
_db = None

def get_client():
    global _client
    if _client is None:
        mongo_uri = os.getenv("MONGO_URI") or os.getenv("MONGODB_URI")
        if not mongo_uri:
            # We don't raise here to allow non-DB routes to work
            return None
        try:
            _client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
            # Test connection immediately
            _client.admin.command('ismaster')
        except Exception as e:
            error_msg = str(e)
            print(f"DATABASE INITIALIZATION ERROR: {error_msg}")
            
            if "SSL handshake failed" in error_msg or "TLSV1_ALERT_INTERNAL_ERROR" in error_msg:
                print("\n" + "!"*60)
                print("CRITICAL: MongoDB SSL Handshake Failed.")
                print("Your IP address is likely not whitelisted in MongoDB Atlas.")
                print("FIX: Go to MongoDB Atlas -> Network Access -> Add IP Address.")
                print("!"*60 + "\n")
            
            # Reset client so we try again next time
            _client = None
            return None
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
        mongo_uri = os.getenv("MONGO_URI") or os.getenv("MONGODB_URI")
        if not mongo_uri:
            print("Database Error: Neither MONGO_URI nor MONGODB_URI is set.")
            return False
            
        client = get_client()
        if not client:
            return False
            
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        return True
    except Exception as e:
        # Diagnostic print already handled in get_client, but keep here for redundancy in health check
        return False

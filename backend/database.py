from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI not found in environment variables. Please check your .env file.")
client = MongoClient(MONGO_URI)
db = client["skillmatch"]

def get_db():
    return db

def get_user_collection():
    return db["users"]

def get_document_collection():
    return db["documents"]

def check_db_connection():
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        return True
    except Exception:
        return False

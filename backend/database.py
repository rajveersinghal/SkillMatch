from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["skillmatch"]

def get_db():
    return db

def get_user_collection():
    return db["users"]

def get_document_collection():
    return db["documents"]

import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
print(f"Testing URI: {mongo_uri}")

try:
    client = MongoClient(mongo_uri)
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("Connection successful!")
except Exception as e:
    print(f"Connection failed: {e}")

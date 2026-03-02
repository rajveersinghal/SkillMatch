from pymongo import MongoClient
import sys

uri = "mongodb+srv://Vercel-Admin-db:lWVKYfkP4SmFbp8Y@db.ws7bgnv.mongodb.net/?retryWrites=true&w=majority"

print(f"Testing connection to: {uri.split('@')[1]}")

try:
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    # Trigger a connection
    client.admin.command('ping')
    print("✅ Successfully connected to MongoDB Atlas!")
    
    db = client["skillmatch"]
    print(f"Testing 'skillmatch' database...")
    
    # Try to write and then delete a test document
    test_col = db["_connection_test"]
    test_id = test_col.insert_one({"test": "ok"}).inserted_id
    print(f"✅ Write access confirmed! (ID: {test_id})")
    test_col.delete_one({"_id": test_id})
    print("✅ Delete access confirmed!")
    
    # Check collections
    collections = db.list_collection_names()
    print(f"Collections in 'skillmatch': {collections}")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    sys.exit(1)
finally:
    client.close()

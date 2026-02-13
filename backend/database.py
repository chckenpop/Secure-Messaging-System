from pymongo import MongoClient
from bson.objectid import ObjectId

MONGO_URL = "mongodb://localhost:27017"

client = MongoClient(MONGO_URL)

db = client["secure_messaging"]
messages_collection = db["messages"]

def store_message(data: dict):
    result = messages_collection.insert_one(data)
    return str(result.inserted_id)

def get_message(message_id: str):
    return messages_collection.find_one({"_id": ObjectId(message_id)})

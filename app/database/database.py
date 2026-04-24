from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL")

if not MONGO_URL:
    raise Exception("❌ MONGO_URL not found in environment variables")

client = MongoClient(MONGO_URL)

db = client["campusDB"]

print("✅ MongoDB Connected")
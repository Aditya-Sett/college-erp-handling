from pymongo import MongoClient
import os

MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["smart_attendance"]

curriculum_collection = db["curriculums"]
print(f"Db connected to {MONGO_URI}")
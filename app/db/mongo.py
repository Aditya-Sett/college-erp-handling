from pymongo import MongoClient
import os

MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["smart_attendance"]

curriculum_collection = db["curriculums"]
students_collection = db["students"]
studentEnrollmentCounts_collection = db["studentEnrollmentCounts"]

print(f"Db connected to {MONGO_URI}")
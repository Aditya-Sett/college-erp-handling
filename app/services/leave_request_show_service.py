from app.db.mongo import db
from bson import ObjectId
from app.connection.connection import BASE_ANALYSIS_URL

leave_request_collection = db["leave_request"]
BASE_URL = f"{BASE_ANALYSIS_URL}/api/analysis/files"
print("BASE_URL", BASE_URL)

def get_leave_requests_by_teacher(teacherId):
    if not teacherId:
        raise Exception("teacherId is required")

    # MongoDB OR query
    query = {
        "$or": [
            {"classCoordinatorId": teacherId},
            {"HODId": teacherId}
        ]
    }

    results = leave_request_collection.find(query)

    response = []

    for doc in results:
        doc["_id"] = str(doc["_id"])  # convert ObjectId to string
        # Convert file path → URL
        if "proof" in doc:
            filename = doc["proof"].split("\\")[-1]  # handle Windows path
            doc["proof_url"] = f"{BASE_URL}/{filename}"
        response.append(doc)

    print("response",response)
    return response
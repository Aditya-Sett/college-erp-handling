from app.db.mongo import db
from app.connection.connection import BASE_ANALYSIS_URL

leave_request_collection = db["leave_request"]
leave_approved_collection = db["leave_approved"]
leave_denied_collection = db["leave_denied"]
BASE_URL = f"{BASE_ANALYSIS_URL}/api/analysis/files"

def get_student_leave_history(studentId):
    if not studentId:
        raise Exception("studentId is required")

    final_data = []

    # 🔹 1. Pending Requests
    pending = list(leave_request_collection.find({"studentId": studentId}))
    for doc in pending:
        doc["_id"] = str(doc["_id"])
        doc["status"] = "PENDING"   # normalize
        # Convert file path → URL
        if "proof" in doc:
            filename = doc["proof"].split("\\")[-1]  # handle Windows path
            doc["proof_url"] = f"{BASE_URL}/{filename}"
        final_data.append(doc)

    # 🔹 2. Approved Leaves
    approved = list(leave_approved_collection.find({"studentId": studentId}))
    for doc in approved:
        doc["_id"] = str(doc["_id"])
        doc["status"] = "APPROVED"
        # Convert file path → URL
        if "proof" in doc:
            filename = doc["proof"].split("\\")[-1]  # handle Windows path
            doc["proof_url"] = f"{BASE_URL}/{filename}"
        final_data.append(doc)

    # 🔹 3. Denied Leaves
    denied = list(leave_denied_collection.find({"studentId": studentId}))
    for doc in denied:
        doc["_id"] = str(doc["_id"])
        doc["status"] = "DENIED"
        # Convert file path → URL
        if "proof" in doc:
            filename = doc["proof"].split("\\")[-1]  # handle Windows path
            doc["proof_url"] = f"{BASE_URL}/{filename}"
        final_data.append(doc)

    # 🔹 Optional: Sort by timestamp (latest first)
    final_data.sort(
        key=lambda x: x.get("timestamp", x.get("approved_timestamp", x.get("denied_timestamp"))),
        reverse=True
    )

    return final_data
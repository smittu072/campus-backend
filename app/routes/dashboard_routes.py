from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import FileResponse
from app.database.database import db
from app.utils.jwt import verify_token
import os

router = APIRouter()

assignments = db["assignments"]
users = db["users"]

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ================= TOKEN =================
def get_user_id(request: Request):
    auth = request.headers.get("Authorization")
    if not auth:
        return None
    token = auth.split(" ")[1]
    payload = verify_token(token)
    return payload.get("id") if payload else None


# ================= STUDENT =================
@router.get("/student")
async def student_dashboard(request: Request):
    user_id = get_user_id(request)

    data = list(assignments.find({"user_id": user_id}))

    return {
        "assignment_list": [
            {
                "title": a.get("title"),
                "status": a.get("status"),
                "deadline": a.get("deadline"),
                "marks": a.get("marks"),
                "file": a.get("file"),
            }
            for a in data
        ]
    }


# ================= 🔥 FACULTY DASHBOARD (FIXED) =================
@router.get("/faculty")
async def faculty_dashboard():
    total_students = users.count_documents({"role": "student"})
    total_assignments = assignments.count_documents({})

    pending = assignments.count_documents({"status": "pending"})
    completed = assignments.count_documents({"status": "completed"})

    return {
        "students": total_students,
        "assignments": total_assignments,
        "pending": pending,
        "completed": completed
    }


# ================= DOWNLOAD =================
@router.get("/download")
async def download_file(file_path: str):
    return FileResponse(file_path)


# ================= FACULTY TABLE =================
@router.get("/faculty-table")
async def faculty_table():
    data = list(assignments.find({}))
    students = {str(s["_id"]): s["name"] for s in users.find({"role": "student"})}

    result = []

    for a in data:
        result.append({
            "student": students.get(a.get("user_id"), "Unknown"),
            "title": a.get("title"),
            "status": a.get("status"),
            "marks": a.get("marks"),
        })

    return result


# ================= ANALYTICS =================
@router.get("/analytics")
async def analytics():
    return {
        "pending": assignments.count_documents({"status": "pending"}),
        "completed": assignments.count_documents({"status": "completed"})
    }


# ================= ADD ASSIGNMENT =================
@router.post("/assignment")
async def add_assignment(data: dict):
    assignments.insert_one({
        "user_id": data.get("student_id"),
        "title": data.get("title"),
        "status": "pending",
        "deadline": data.get("deadline"),
        "marks": None,
        "file": None
    })
    return {"msg": "Assignment added"}


# ================= FILE SUBMIT =================
@router.post("/submit-assignment")
async def submit_assignment(
    request: Request,
    title: str,
    file: UploadFile = File(...)
):
    user_id = get_user_id(request)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    assignments.update_one(
        {"user_id": user_id, "title": title},
        {
            "$set": {
                "status": "completed",
                "file": file_path
            }
        }
    )

    return {"msg": "Submitted"}


# ================= MARKS =================
@router.post("/assign-marks")
async def assign_marks(data: dict):
    assignments.update_one(
        {"user_id": data.get("student_id"), "title": data.get("title")},
        {"$set": {"marks": data.get("marks")}}
    )
    return {"msg": "Marks updated"}

@router.get("/students")
async def get_students():
    all_students = list(users.find({"role": "student"}))

    return [
        {
            "enroll": s.get("enroll", "N/A"),
            "name": s.get("name"),
            "email": s.get("email")
        }
        for s in all_students
    ]
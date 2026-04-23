from fastapi import APIRouter
from app.database.database import db

router = APIRouter()

timetable = db["timetable"]
assignments = db["assignments"]
attendance = db["attendance"]

# ✅ TIMETABLE
@router.post("/timetable")
async def save_timetable(data: dict):
    timetable.insert_one(data)
    return {"msg": "Timetable saved"}

# ✅ ASSIGNMENT
@router.post("/assignment")
async def add_assignment(data: dict):
    assignments.insert_one(data)
    return {"msg": "Assignment added"}

# ✅ ATTENDANCE
@router.post("/attendance")
async def update_attendance(data: dict):
    attendance.insert_one(data)
    return {"msg": "Attendance updated"}
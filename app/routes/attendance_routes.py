from fastapi import APIRouter
from app.database.database import db

router = APIRouter()
attendance = db["attendance"]

@router.post("/update")
async def update_attendance(data: dict):
    attendance.insert_one(data)
    return {"msg": "Attendance updated"}
from fastapi import APIRouter
from app.database.database import db

router = APIRouter()

notices = db["notices"]

@router.post("/add")
async def add_notice(data: dict):
    notices.insert_one(data)
    return {"msg": "Notice added"}
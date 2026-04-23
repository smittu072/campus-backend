from fastapi import APIRouter
from app.database.database import db

router = APIRouter()

assignments = db["assignments"]

@router.post("/add")
async def add_assignment(data: dict):
    assignments.insert_one(data)
    return {"msg": "Assignment added"}
from fastapi import APIRouter
from app.controllers.auth_controller import signup, login

router = APIRouter()

@router.post("/signup")
async def signup_route(data: dict):
    return await signup(data)

@router.post("/login")
async def login_route(data: dict):
    return await login(data)
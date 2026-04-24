from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ROUTES
from app.routes import dashboard_routes
from app.routes import student_routes
from app.routes import auth_routes
from app.routes import assignment_routes
from app.routes import notice_routes
from app.routes import attendance_routes
from app.routes import ai_routes

# WEBSOCKET
from app.websocket import dashboard_ws

app = FastAPI()

# ✅ CORS (frontend deploy ke baad restrict karna)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later change to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ HEALTH CHECK (IMPORTANT for Render)
@app.get("/")
def root():
    return {"status": "Backend Running 🚀"}

# ✅ ROUTES
app.include_router(dashboard_routes.router, prefix="/api/dashboard")
app.include_router(student_routes.router, prefix="/api/student")
app.include_router(auth_routes.router, prefix="/api/auth")
app.include_router(assignment_routes.router, prefix="/api/assignment")
app.include_router(notice_routes.router, prefix="/api/notice")
app.include_router(attendance_routes.router, prefix="/api/attendance")
app.include_router(ai_routes.router, prefix="/api/ai")

# ✅ WEBSOCKET
app.include_router(dashboard_ws.router)
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.teacher import router as teacher_router
from app.api.student import router as student_router
from app.api.auth import router as auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)



app.include_router(teacher_router)

app.include_router(student_router)

app.include_router(auth_router)

from fastapi import FastAPI
from app.api.teacher import router as teacher_router
from app.api.student import router as student_router
from app.database import Base, engine


app = FastAPI()

Base.metadata.create_all(bind = engine)

app.include_router(teacher_router)

app.include_router(student_router)


from fastapi import FastAPI
from app.api.teacher import router as teacher_router
from app.database import Base, engine
from app.models import Teacher, Student, Course, Workshop, Enrollment, Video, Progress


app = FastAPI()

Base.metadata.create_all(bind = engine)

app.include_router(teacher_router)


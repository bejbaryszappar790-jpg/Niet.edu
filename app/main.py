from fastapi import FastAPI
from app.schemas import courses

app = FastAPI()


@app.post("/courses")
def create_courses()